import re
from docx import Document

FILE = r"E:\আমাদের কোরআন\কোরআনের অনুবাদ\সূরা ১ আল-ফাতিহা.docx"


# বাংলা সংখ্যা → ইংরেজি সংখ্যা
def normalize_number(text):
    bengali_digits = "০১২৩৪৫৬৭৮৯"
    english_digits = "0123456789"

    table = str.maketrans(
        bengali_digits,
        english_digits
    )

    return text.translate(table)


# DOCX পড়া
doc = Document(FILE)

ayahs = []
current_ayah = None
current_text = []


for paragraph in doc.paragraphs:

    # একটি paragraph-এর মধ্যে একাধিক line থাকলেও আলাদা করে দেখব
    lines = paragraph.text.splitlines()

    for line in lines:

        line = line.strip()

        # খালি লাইন বাদ
        if not line:
            continue

        # ** চিহ্ন থাকলে বাদ
        line = line.replace("**", "")

        # আয়াতের শুরু খুঁজব
        match = re.match(
            r"^\s*([০-৯0-9]+)\s*[\.\।]\s*(.*)$",
            line
        )

        if match:

            # আগের আয়াত সংরক্ষণ
            if current_ayah is not None:

                ayahs.append({
                    "number": current_ayah,
                    "translation": " ".join(current_text).strip()
                })

            # নতুন আয়াত
            number_text = match.group(1)
            text = match.group(2).strip()

            current_ayah = int(
                normalize_number(number_text)
            )

            current_text = [text]

        else:

            # আয়াত শুরু হওয়ার পরের লাইন হলে
            # সেটি আগের আয়াতের অংশ
            if current_ayah is not None:
                current_text.append(line)


# শেষ আয়াত সংরক্ষণ
if current_ayah is not None:

    ayahs.append({
        "number": current_ayah,
        "translation": " ".join(current_text).strip()
    })


# ফলাফল দেখানো
print()
print("======================================")
print("সূরা ১ — অনুবাদ পরীক্ষা")
print("======================================")

print()

for ayah in ayahs:

    print(
        f"{ayah['number']}. {ayah['translation']}"
    )

print()
print("======================================")
print(f"মোট আয়াত পাওয়া গেছে: {len(ayahs)}")
print("======================================")