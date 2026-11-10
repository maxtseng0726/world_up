from pathlib import Path
import re
import sqlite3
import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "public" / "main.pdf"
DB_PATH = ROOT / "database" / "vocabulary.db"

# The PDF's level headings are authoritative.
LEVEL_PATTERN = re.compile(
    r"LEVEL\s*([1-6])\s*\([\d,]+\s+words\)",
    re.IGNORECASE,
)

# A vocabulary entry begins with a word/expression,
# optionally followed by phonetic text in square brackets.
ENTRY_PATTERN = re.compile(
    r"^(?P<word>.+?)\s+"
    r"\[(?P<phonetic>[^\]]+)\]"
    r"(?P<rest>.*)$"
)


POS_PATTERN = re.compile(
    r"(?<![A-Za-z])"
    r"(?:vt|vi|aux|art|pron|adj|adv|prep|conj|interj|"
    r"n|v|a)"
    r"\.?"
    r"(?![A-Za-z])"
    r"\s*",
    re.IGNORECASE,
)

def parse_entry(text, level):
    text = re.sub(r"\s+", " ", text).strip()

    match = ENTRY_PATTERN.match(text)
    if not match:
        return None

    word = match.group("word").strip()
    phonetic = match.group("phonetic").strip()
    rest = match.group("rest").strip()

    # Capture additional phonetic forms, such as / [ˋæktrɪs].
    extra_phonetics = re.match(
        r"^(?:\s*/\s*\[[^\]]+\]\s*)+",
        rest,
    )

    if extra_phonetics:
        phonetic += " " + extra_phonetics.group(0).strip()
        rest = rest[extra_phonetics.end():].strip()

    # Extract POS only at the beginning of the remaining text.
    pos_match = POS_PATTERN.match(rest)

    if pos_match:
        pos = pos_match.group(0).strip()
        meaning = rest[pos_match.end():].strip()
    else:
        pos = None
        meaning = rest

    return (
        word,
        phonetic or None,
        pos,
        meaning or "[REVIEW]",
        level,
    )

def extract_entries():
    records = []
    current_level = 1
    review_lines = []

    with pdfplumber.open(PDF_PATH) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            full_text = page.extract_text() or ""
            heading = LEVEL_PATTERN.search(full_text)

            if heading:
                current_level = int(heading.group(1))

            midpoint = page.width / 2

            columns = [
                page.crop((0, 0, midpoint - 2, page.height)).extract_text() or "",
                page.crop((midpoint + 2, 0, page.width, page.height)).extract_text() or "",
            ]

            for column_text in columns:
                pending = ""

                for raw_line in column_text.splitlines():
                    line = raw_line.strip()

                    if not line:
                        continue

                    if "大考中心字彙表" in line or LEVEL_PATTERN.search(line):
                        continue

                    # A new entry starts with a word followed by phonetics.
                    if ENTRY_PATTERN.match(line):
                        if pending:
                            record = parse_entry(pending, current_level)
                            if record:
                                records.append(record)
                            else:
                                review_lines.append((page_no, current_level, pending))

                        pending = line

                    # A wrapped line belongs to the preceding entry.
                    elif pending:
                        pending += " " + line

                    else:
                        review_lines.append((page_no, current_level, line))

                if pending:
                    record = parse_entry(pending, current_level)
                    if record:
                        records.append(record)
                    else:
                        review_lines.append((page_no, current_level, pending))

    return records, review_lines


def main():
    if not PDF_PATH.exists():
        raise FileNotFoundError(PDF_PATH)

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    records, review_lines = extract_entries()

    print("Source:", PDF_PATH)
    print("Candidate records:", len(records))
    print("Lines needing review:", len(review_lines))

    print("\n--- Preview: first 15 records ---")
    for record in records[:15]:
        print(record)

    print("\n--- Preview: first 15 review lines ---")
    for item in review_lines[:15]:
        print(item)

    answer = input(
        "\nPreview only. Import these records into SQLite? "
        "Type YES to continue: "
    ).strip()

    if answer != "YES":
        print("Cancelled. Database was not changed.")
        return

    with sqlite3.connect(DB_PATH) as conn:
        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(words)")
        }

        required = {
            "word", "phonetic", "pos", "meaning", "level"
        }
        if not required.issubset(columns):
            raise RuntimeError(
                f"words table is missing columns: "
                f"{required - columns}"
            )

        # Refuse to overwrite existing rows automatically.
        existing = conn.execute(
            "SELECT COUNT(*) FROM words"
        ).fetchone()[0]

        if existing:
            raise RuntimeError(
                f"words already contains {existing} rows. "
                "Import cancelled to protect existing data."
            )

        conn.executemany(
            """
            INSERT INTO words
                (word, phonetic, pos, meaning, level)
            VALUES (?, ?, ?, ?, ?)
            """,
            records,
        )

        print("\nImported records by level:")
        for row in conn.execute(
            """
            SELECT level, COUNT(*)
            FROM words
            GROUP BY level
            ORDER BY level
            """
        ):
            print(f"Level {row[0]}: {row[1]}")


if __name__ == "__main__":
    main()
