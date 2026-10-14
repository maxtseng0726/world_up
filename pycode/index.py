import re
import subprocess
from pathlib import Path
from pypdf import PdfReader, PdfWriter


# =========================
# 用 macOS 原生視窗選擇 PDF
# =========================

def select_pdf():
    script = '''
    tell application "System Events"
        activate
        set selectedFile to choose file ¬
            with prompt "請選擇要拆分的 PDF" ¬
            of type {"com.adobe.pdf"}
        return POSIX path of selectedFile
    end tell
    '''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    return result.stdout.strip()


# =========================
# 選擇 PDF
# =========================

input_file = select_pdf()

if not input_file:
    print("沒有選擇 PDF，程式結束。")
    exit()

print(f"選擇的 PDF：{input_file}")


# =========================
# 建立輸出資料夾
# =========================

input_path = Path(input_file)

output_dir = input_path.parent

output_dir.mkdir(exist_ok=True)


# =========================
# 讀取 PDF
# =========================

reader = PdfReader(input_file)

print(f"PDF 共 {len(reader.pages)} 頁")


# =========================
# 找 LEVEL 標題
# =========================

levels = []

for page_index, page in enumerate(reader.pages):

    text = page.extract_text() or ""

    # 找：
    # 大考中心字彙表 LEVEL 1
    # 大考中心字彙表 LEVEL 2
    # ...
    matches = re.finditer(
        r"大考中心字彙表\s*LEVEL\s*(\d+)",
        text,
        re.IGNORECASE
    )

    for match in matches:

        level_number = int(match.group(1))

        levels.append({
            "level": level_number,
            "page": page_index,
            "position": match.start()
        })


# =========================
# 檢查
# =========================

if not levels:

    print()
    print("找不到 LEVEL 標題。")
    print()
    print("可能原因：")
    print("- PDF 是掃描圖片")
    print("- PDF 文字無法正常擷取")
    print("- 標題格式和程式設定不同")

    exit()


# 按照 PDF 順序排序

levels.sort(
    key=lambda x: (
        x["page"],
        x["position"]
    )
)


# =========================
# 顯示偵測結果
# =========================

print()
print("找到的 LEVEL：")

for item in levels:

    print(
        f"LEVEL {item['level']} "
        f"→ 第 {item['page'] + 1} 頁"
    )


# =========================
# 開始拆分
# =========================

for i, current in enumerate(levels):

    level = current["level"]

    start_page = current["page"]


    # 下一個 LEVEL
    if i + 1 < len(levels):

        next_level = levels[i + 1]

        end_page = next_level["page"]

    else:

        end_page = len(reader.pages)


    # 建立 PDF writer

    writer = PdfWriter()


    # 加入頁面

    for page_number in range(
        start_page,
        end_page
    ):

        writer.add_page(
            reader.pages[page_number]
        )


    # 輸出檔名

    output_file = (
        output_dir /
        f"lv{level}_vocab.pdf"
    )


    with open(output_file, "wb") as f:

        writer.write(f)


    print(
        f"✓ lv{level}_vocab.pdf "
        f"（第 {start_page + 1}～{end_page} 頁）"
    )


# =========================
# 完成
# =========================

print()
print("==============================")
print("拆分完成！")
print("==============================")
print()
print(f"輸出位置：")
print(output_dir)
