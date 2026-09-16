import os
import re
import json
from docx import Document


# =========================================
# ফোল্ডার
# =========================================

SOURCE_FOLDER = r"E:\আমাদের কোরআন\কোরআনের অনুবাদ"

OUTPUT_FILE = r"E:\আমাদের কোরআন\data\translation_bn.json"

QURAN_FILE = r"E:\আমাদের কোরআন\quran.json"


# =========================================
# বাংলা সংখ্যা → ইংরেজি সংখ্যা
# =========================================

def normalize_number(text):

    bengali_digits = "০১২৩৪৫৬৭৮৯"
    english_digits = "0123456789"

    table = str.maketrans(
        bengali_digits,
        english_digits
    )

    return text.translate(table)


# =========================================
# একটি DOCX থেকে আয়াত বের করা
# =========================================

def read_surah_docx(file_path):

    doc = Document(file_path)

    ayahs = []

    current_ayah = None
    current_text = []

    for paragraph in doc.paragraphs:

        lines = paragraph.text.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Markdown-এর ** থাকলে বাদ
            line = line.replace("**", "")

            # আয়াত নম্বর খোঁজা
            match = re.match(
                r"^\s*([০-৯0-9]+)\s*[\.\।]\s*(.*)$",
                line
            )

            if match:

                # আগের আয়াত সংরক্ষণ
                if current_ayah is not None:

                    ayahs.append({
                        "number": current_ayah,
                        "translation": " ".join(
                            current_text
                        ).strip()
                    })

                number_text = match.group(1)

                text = match.group(2).strip()

                current_ayah = int(
                    normalize_number(number_text)
                )

                current_text = [text]

            else:

                # আয়াতের পরের লাইন হলে
                # সেটি একই আয়াতের অংশ
                if current_ayah is not None:

                    current_text.append(line)

    # শেষ আয়াত
    if current_ayah is not None:

        ayahs.append({
            "number": current_ayah,
            "translation": " ".join(
                current_text
            ).strip()
        })

    return ayahs


# =========================================
# quran.json পড়া
# =========================================

print()
print("Quran JSON পড়া হচ্ছে...")

with open(
    QURAN_FILE,
    "r",
    encoding="utf-8"
) as f:

    quran_data = json.load(f)


# =========================================
# DOCX ফাইল সংগ্রহ
# =========================================

files = []

for filename in os.listdir(SOURCE_FOLDER):

    if filename.lower().endswith(".docx"):

        # filename থেকে সূরা নম্বর
        match = re.search(
            r"সূরা\s*([০-৯0-9]+)",
            filename
        )

        if match:

            number = int(
                normalize_number(
                    match.group(1)
                )
            )

            files.append(
                (number, filename)
            )


files.sort(
    key=lambda x: x[0]
)


print(
    f"মোট DOCX ফাইল পাওয়া গেছে: {len(files)}"
)

print()


# =========================================
# Translation database
# =========================================

translation_data = {}


# =========================================
# প্রতিটি সূরা পড়া
# =========================================

success_count = 0


for surah_number, filename in files:

    file_path = os.path.join(
        SOURCE_FOLDER,
        filename
    )

    print(
        f"প্রক্রিয়া করা হচ্ছে: "
        f"সূরা {surah_number} — {filename}"
    )

    try:

        ayahs = read_surah_docx(
            file_path
        )

        # quran.json থেকে সূরার নাম
        quran_surah = quran_data.get(
            str(surah_number),
            {}
        )

        name_bn = quran_surah.get(
            "name_bn",
            ""
        )

        translation_data[
            str(surah_number)
        ] = {

            "name_bn": name_bn,

            "ayahs": ayahs
        }

        print(
            f"   ✓ আয়াত পাওয়া গেছে: "
            f"{len(ayahs)}"
        )

        success_count += 1

    except Exception as e:

        print(
            f"   ✗ সমস্যা: {e}"
        )


# =========================================
# data folder নিশ্চিত করা
# =========================================

output_folder = os.path.dirname(
    OUTPUT_FILE
)

os.makedirs(
    output_folder,
    exist_ok=True
)


# =========================================
# JSON তৈরি
# =========================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        translation_data,
        f,
        ensure_ascii=False,
        indent=4
    )


# =========================================
# শেষ রিপোর্ট
# =========================================

print()
print("======================================")
print("কাজ সম্পন্ন")
print("======================================")

print(
    f"মোট DOCX: {len(files)}"
)

print(
    f"সফলভাবে পড়া হয়েছে: {success_count}"
)

print(
    f"JSON তৈরি হয়েছে:"
)

print(
    OUTPUT_FILE
)

print("======================================")