import json
from pathlib import Path

BASE = Path(r"E:\আমাদের কোরআন")

source_file = BASE / "quran-uthmani.txt"
output_file = BASE / "data" / "quran.json"

# ১১৪টি সূরার আয়াত সংখ্যা
SURAH_AYAH_COUNTS = [
    7, 286, 200, 176, 120, 165, 206, 75, 129, 109,
    123, 111, 43, 52, 99, 128, 111, 110, 98, 135,
    112, 78, 118, 64, 77, 227, 93, 88, 69, 60,
    34, 30, 73, 54, 45, 83, 182, 88, 75, 85,
    54, 53, 89, 59, 37, 35, 38, 29, 18, 45,
    60, 49, 62, 55, 78, 96, 29, 22, 24, 13,
    14, 11, 11, 18, 12, 12, 30, 52, 52, 44,
    28, 28, 20, 56, 40, 31, 50, 40, 46, 42,
    29, 19, 36, 25, 22, 17, 19, 26, 30, 20,
    15, 21, 11, 8, 8, 19, 5, 8, 8, 11,
    11, 8, 3, 9, 5, 4, 7, 3, 6, 3,
    5, 4, 5, 6
]
BISMILLAH = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِیمِ"
def remove_bismillah(text):
    normalized = text.replace("ّ", "").replace("ۡ", "").replace("َ", "").replace("ِ", "").replace("ُ", "").replace("ٰ", "")

    bismillah_normalized = "بسم الله الرحمن الرحیم"

    if normalized.startswith(bismillah_normalized):
        # মূল লেখার প্রথম অংশ থেকে বিসমিল্লাহ বাদ দেওয়ার জন্য
        words = text.split()
        if len(words) >= 4:
            return " ".join(words[4:]).strip()

    return text
# quran-uthmani.txt পড়া
text = source_file.read_text(encoding="utf-8")

lines = [
    line.strip()
    for line in text.splitlines()
    if line.strip()
]

print("মোট আয়াত/লাইন পাওয়া গেছে:", len(lines))

expected_total = sum(SURAH_AYAH_COUNTS)

if len(lines) != expected_total:
    print("সতর্কতা!")
    print("প্রত্যাশিত:", expected_total)
    print("পাওয়া গেছে:", len(lines))
    raise SystemExit

# ফলাফল
quran = {}

position = 0

for surah_number, ayah_count in enumerate(SURAH_AYAH_COUNTS, start=1):

    surah_lines = lines[position:position + ayah_count]

    position += ayah_count

    ayahs = []

    for ayah_number, ayah_text in enumerate(surah_lines, start=1):

        # সূরা ১-এর প্রথম লাইনটি বিসমিল্লাহ।
        # এটি আপনার অনুবাদের কাঠামোর সঙ্গে রাখা হবে।
        if surah_number == 1:
            pass

        # সূরা ২–১১৪-এর প্রথম আয়াতের শুরুতে
        # বিসমিল্লাহ থাকলে সেটি বাদ দেওয়া হবে।
        elif ayah_number == 1 and surah_number != 9:
            words = ayah_text.split()

            if len(words) >= 4:
                ayah_text = " ".join(words[4:]).strip()

        ayahs.append({
            "number": ayah_number,
            "text": ayah_text
        })

    quran[str(surah_number)] = {
        "ayahs": ayahs
    }

# JSON সংরক্ষণ
output_file.parent.mkdir(parents=True, exist_ok=True)

output_file.write_text(
    json.dumps(quran, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print()
print("===================================")
print("সব ১১৪ সূরা সফলভাবে তৈরি হয়েছে।")
print("===================================")

print()
print("পরীক্ষা:")

print("সূরা ১:", len(quran["1"]["ayahs"]), "আয়াত")
print("সূরা ২:", len(quran["2"]["ayahs"]), "আয়াত")
print("সূরা ৯:", len(quran["9"]["ayahs"]), "আয়াত")
print("সূরা ১১৪:", len(quran["114"]["ayahs"]), "আয়াত")

print()
print("সূরা ২-এর প্রথম আয়াত:")
print(quran["2"]["ayahs"][0]["text"])

print()
print("সূরা ৩-এর প্রথম আয়াত:")
print(quran["3"]["ayahs"][0]["text"])

print()
print("সূরা ১০-এর প্রথম আয়াত:")
print(quran["10"]["ayahs"][0]["text"])

print()
print("JSON তৈরি হয়েছে:")
print(output_file)