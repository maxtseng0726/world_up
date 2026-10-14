import re
import sqlite3
from pathlib import Path

from pypdf import PdfReader


# ============================================================
# 路徑
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

PDF_DIR = ROOT / "public"
DB_DIR = ROOT / "database"
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "vocabulary.db"


# ============================================================
# 設定
# ============================================================

LEVELS = {
    1: 1080,
    2: 1080,
    3: 1080,
    4: 1080,
    5: 1080,
}

POS_PATTERN = re.compile(
    r"^(?:(?:adj|adv|art|conj|prep|pron|n|v|vt|vi|aux|"
    r"modal|phr|phrase|abbr|num)\.?(?:\s*/\s*)?)+",
    re.IGNORECASE,
)

# 常見詞性
POS_WORDS = {
    "n.",
    "v.",
    "vt.",
    "vi.",
    "adj.",
    "adv.",
    "prep.",
    "conj.",
    "pron.",
    "art.",
    "aux.",
    "num.",
}

# PDF 中不應該被當成單字的東西
INVALID_WORDS = {
    "level",
    "page",
    "contents",
    "word",
    "meaning",
    "n.",
    "v.",
    "vt.",
    "vi.",
    "adj.",
    "adv.",
    "prep.",
    "conj.",
    "pron.",
    "art.",
}


# ============================================================
# 基本清理
# ============================================================

def clean_spaces(text: str) -> str:
    """
    清理 PDF 常見的多餘空白。
    """
    text = text.replace("\xa0", " ")
    text = text.replace("\t", " ")

    # 多個空白 -> 一個
    text = re.sub(r"[ ]{2,}", " ", text)

    return text.strip()


def clean_pronunciation(text: str) -> str:
    """
    清理音標。
    """

    text = text.strip()

    # [ xxx ] -> xxx
    text = re.sub(r"^\[\s*", "", text)
    text = re.sub(r"\s*\]$", "", text)

    # / [xxx] -> / xxx
    text = re.sub(r"\]\s*/\s*\[", " / ", text)

    text = re.sub(r"\s*/\s*", " / ", text)

    return clean_spaces(text)


def clean_pos(text: str) -> str:
    """
    清理詞性。
    """

    text = clean_spaces(text)

    return text


def clean_meaning(text: str) -> str:
    """
    清理中文意思。
    """

    text = clean_spaces(text)

    return text


# ============================================================
# 判斷
# ============================================================

def looks_like_word(line: str) -> bool:
    """
    判斷一行是否可能是單字開頭。
    """

    if not line:
        return False

    first = line.split()[0]

    if first.lower() in INVALID_WORDS:
        return False

    # 純詞性
    if first.lower() in POS_WORDS:
        return False

    # 必須至少含英文字母
    if not re.search(r"[A-Za-z]", first):
        return False

    return True


def extract_word_and_rest(line: str):
    """
    從一行中抓出：
        word
        剩餘內容

    支援：

        able [xxx] adj. 能，可以
        according to [xxx] 根據
        actor/actress [xxx] n. 男演員/女演員
        account1 [xxx] n. 帳戶
        AI/artificial intelligence [xxx] n. 人工智慧
    """

    line = clean_spaces(line)

    if not line:
        return None, ""

    if not looks_like_word(line):
        return None, ""

    # --------------------------------------------------------
    # 找音標開始位置
    #
    # 例：
    #
    # able [ˋeb!] adj. 能，可以
    #
    # word = able
    # rest = [ˋeb!] adj. 能，可以
    # --------------------------------------------------------

    pronunciation_match = re.search(r"\[", line)

    if pronunciation_match:
        before_pron = line[:pronunciation_match.start()].strip()
        rest = line[pronunciation_match.start():].strip()

        # word 通常就是音標前面的全部內容
        word = before_pron

        if word:
            return word, rest

    # --------------------------------------------------------
    # 如果沒有 [ 音標
    #
    # 嘗試從第一個可能的詞性開始切
    # --------------------------------------------------------

    pos_match = re.search(
        r"\b(?:n|v|vt|vi|adj|adv|prep|conj|pron|art)\.",
        line,
        re.IGNORECASE,
    )

    if pos_match:
        word = line[:pos_match.start()].strip()
        rest = line[pos_match.start():].strip()

        if word:
            return word, rest

    # --------------------------------------------------------
    # 最後才用空白切
    # --------------------------------------------------------

    parts = line.split(maxsplit=1)

    word = parts[0]

    if len(parts) == 2:
        rest = parts[1]
    else:
        rest = ""

    return word, rest


# ============================================================
# 解析一個詞條
# ============================================================

def parse_entry(lines, index):
    """
    從 lines[index] 開始嘗試解析一個完整詞條。

    回傳：

        {
            "word": ...,
            "pronunciation": ...,
            "part_of_speech": ...,
            "meaning": ...,
        }

    或 None
    """

    line = clean_spaces(lines[index])

    word, rest = extract_word_and_rest(line)

    if not word:
        return None

    # 避免明顯不是單字
    if word.lower() in INVALID_WORDS:
        return None

    pronunciation = ""
    part_of_speech = ""
    meaning = ""

    # ========================================================
    # 1. 處理音標
    # ========================================================

    pron_match = re.search(
        r"\[(.*?)\]",
        rest,
        re.DOTALL,
    )

    if pron_match:

        pronunciation = clean_pronunciation(
            pron_match.group(1)
        )

        after_pron = rest[
            pron_match.end():
        ].strip()

    else:
        after_pron = rest

    # ========================================================
    # 2. 判斷詞性
    # ========================================================

    pos_match = POS_PATTERN.match(after_pron)

    if pos_match:

        part_of_speech = clean_pos(
            pos_match.group(0)
        )

        meaning = after_pron[
            pos_match.end():
        ].strip()

    else:

        # 某些資料沒有明確詞性
        meaning = after_pron.strip()

    # ========================================================
    # 3. 如果 meaning 為空，看看下一行
    # ========================================================

    if not meaning and index + 1 < len(lines):

        next_line = clean_spaces(
            lines[index + 1]
        )

        # 下一行通常是：
        #
        # n. 男演員/女演員
        #
        # 或
        #
        # 男演員/女演員
        #

        next_pos = POS_PATTERN.match(next_line)

        if next_pos:

            if not part_of_speech:

                part_of_speech = clean_pos(
                    next_pos.group(0)
                )

            meaning = next_line[
                next_pos.end():
            ].strip()

        elif next_line:

            meaning = next_line

    # ========================================================
    # 4. 清理
    # ========================================================

    word = clean_spaces(word)

    pronunciation = clean_pronunciation(
        pronunciation
    )

    part_of_speech = clean_pos(
        part_of_speech
    )

    meaning = clean_meaning(
        meaning
    )

    # ========================================================
    # 5. 基本驗證
    # ========================================================

    if not word:
        return None

    if word.lower() in INVALID_WORDS:
        return None

    if not re.search(r"[A-Za-z]", word):
        return None

    return {
        "word": word,
        "pronunciation": pronunciation,
        "part_of_speech": part_of_speech,
        "meaning": meaning,
    }


# ============================================================
# 建立資料庫
# ============================================================

def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS words
    """)

    cursor.execute("""
        CREATE TABLE words (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL,
            pronunciation TEXT,
            part_of_speech TEXT,
            meaning TEXT NOT NULL,
            level INTEGER NOT NULL
        )
    """)

    conn.commit()

    return conn


# ============================================================
# 讀取 PDF
# ============================================================

def extract_pdf_lines(pdf_path):

    reader = PdfReader(pdf_path)

    lines = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text() or ""

        if not text.strip():
            continue

        page_lines = text.splitlines()

        for line in page_lines:

            line = line.strip()

            if line:
                lines.append(line)

    return lines, len(reader.pages)


# ============================================================
# 匯入 LEVEL
# ============================================================

def import_level(
    conn,
    level,
    pdf_path,
):

    print()
    print("=" * 60)
    print(f"LEVEL {level}")
    print("=" * 60)

    print(f"檔案：{pdf_path}")

    lines, page_count = extract_pdf_lines(
        pdf_path
    )

    print(f"頁數：{page_count}")

    cursor = conn.cursor()

    candidates = 0
    imported = 0

    i = 0

    while i < len(lines):

        line = lines[i]

        # ----------------------------------------------------
        # 跳過頁首
        # ----------------------------------------------------

        if "大考中心字彙表" in line:
            i += 1
            continue

        if re.match(
            r"^LEVEL\s+\d+",
            line,
            re.IGNORECASE,
        ):
            i += 1
            continue

        # ----------------------------------------------------
        # 嘗試解析
        # ----------------------------------------------------

        entry = parse_entry(
            lines,
            i,
        )

        if entry is None:

            i += 1
            continue

        candidates += 1

        # ----------------------------------------------------
        # 如果 meaning 是空的
        # 再嘗試下一行
        # ----------------------------------------------------

        if (
            not entry["meaning"]
            and i + 1 < len(lines)
        ):

            next_line = clean_spaces(
                lines[i + 1]
            )

            if next_line:

                next_pos = POS_PATTERN.match(
                    next_line
                )

                if next_pos:

                    entry["part_of_speech"] = (
                        clean_pos(
                            next_pos.group(0)
                        )
                    )

                    entry["meaning"] = (
                        clean_meaning(
                            next_line[
                                next_pos.end():
                            ]
                        )
                    )

                    i += 1

                else:

                    entry["meaning"] = (
                        clean_meaning(
                            next_line
                        )
                    )

                    i += 1

        # ----------------------------------------------------
        # meaning 還是沒有
        # ----------------------------------------------------

        if not entry["meaning"]:

            print(
                f"警告：沒有 meaning："
                f"{entry['word']}"
            )

            i += 1
            continue

        # ----------------------------------------------------
        # 防止詞性被當成 word
        # ----------------------------------------------------

        if entry["word"].lower() in POS_WORDS:

            i += 1
            continue

        # ----------------------------------------------------
        # INSERT
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO words (
                word,
                pronunciation,
                part_of_speech,
                meaning,
                level
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                entry["word"],
                entry["pronunciation"],
                entry["part_of_speech"],
                entry["meaning"],
                level,
            ),
        )

        imported += 1

        i += 1

    conn.commit()

    print(f"找到候選資料：{candidates}")
    print(f"成功匯入：{imported}")

    expected = LEVELS.get(level)

    if expected:

        print(f"參考數量：{expected}")
        print(
            f"差異：{imported - expected}"
        )

    return imported


# ============================================================
# 驗證
# ============================================================

def validate_database(conn):

    cursor = conn.cursor()

    print()
    print("=" * 60)
    print("資料庫驗證")
    print("=" * 60)

    # --------------------------------------------------------
    # 每級數量
    # --------------------------------------------------------

    print()
    print("每級數量：")

    rows = cursor.execute("""
        SELECT level, COUNT(*)
        FROM words
        GROUP BY level
        ORDER BY level
    """).fetchall()

    for level, count in rows:

        print(
            f"LEVEL {level}: {count}"
        )

    # --------------------------------------------------------
    # 空 pronunciation
    # --------------------------------------------------------

    no_pron = cursor.execute("""
        SELECT COUNT(*)
        FROM words
        WHERE pronunciation IS NULL
           OR pronunciation = ''
    """).fetchone()[0]

    print()
    print(
        f"沒有 pronunciation：{no_pron}"
    )

    # --------------------------------------------------------
    # 空 POS
    # --------------------------------------------------------

    no_pos = cursor.execute("""
        SELECT COUNT(*)
        FROM words
        WHERE part_of_speech IS NULL
           OR part_of_speech = ''
    """).fetchone()[0]

    print(
        f"沒有 part_of_speech：{no_pos}"
    )

    # --------------------------------------------------------
    # 空 meaning
    # --------------------------------------------------------

    no_meaning = cursor.execute("""
        SELECT COUNT(*)
        FROM words
        WHERE meaning IS NULL
           OR meaning = ''
    """).fetchone()[0]

    print(
        f"沒有 meaning：{no_meaning}"
    )

    # --------------------------------------------------------
    # 詞性誤當 word
    # --------------------------------------------------------

    bad_words = cursor.execute("""
        SELECT id, word, pronunciation,
               part_of_speech, meaning, level
        FROM words
        WHERE word IN (
            'n.',
            'v.',
            'vt.',
            'vi.',
            'adj.',
            'adv.',
            'prep.',
            'conj.',
            'pron.',
            'art.'
        )
    """).fetchall()

    print()
    print(
        f"疑似詞性誤當單字：{len(bad_words)}"
    )

    for row in bad_words[:20]:

        print(row)

    # --------------------------------------------------------
    # 重複
    # --------------------------------------------------------

    duplicates = cursor.execute("""
        SELECT word, level, COUNT(*)
        FROM words
        GROUP BY word, level
        HAVING COUNT(*) > 1
        ORDER BY level, word
    """).fetchall()
    print()
    print(
        f"重複 word：{len(duplicates)}"
    )
    for row in duplicates[:30]:
        print(row)
    # --------------------------------------------------------
    # 可疑 word
    # --------------------------------------------------------
    suspicious = cursor.execute("""
        SELECT id, word, meaning, level
        FROM words
        WHERE length(word) <= 1
           OR word LIKE '% % %'
        ORDER BY level, id
    """).fetchall()

    print()
    print(
        f"可疑 word：{len(suspicious)}"
    )

    for row in suspicious[:30]:
        print(row)

# ============================================================
# 主程式
# ============================================================

def main():
    print()
    print("=" * 60)
    print("PDF → SQLite")
    print("=" * 60)
    conn = create_database()
    total = 0
    for level in range(1, 6):

        pdf_path = (
            PDF_DIR
            / f"lv{level}_vocab.pdf"
        )

        if not pdf_path.exists():

            print()
            print(
                f"找不到：{pdf_path}"
            )

            continue

        imported = import_level(
            conn,
            level,
            pdf_path,
        )

        total += imported

    # --------------------------------------------------------
    # 驗證
    # --------------------------------------------------------

    validate_database(conn)

    conn.close()

    print()
    print("=" * 60)
    print("完成")
    print("=" * 60)

    print(
        f"總匯入：{total}"
    )

    print(f"資料庫：{DB_PATH}")
if __name__ == "__main__":
    main()
