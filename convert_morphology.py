import json
import os
import re


SOURCE_FILE = "quran-morphology.txt"
QURAN_FILE = "quran-uthmani.txt"
OUTPUT_DIR = "morphology"
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

# Quranic Arabic Corpus / Buckwalter → Arabic
BW_MAP = {
    "'": "ء",
    "|": "آ",
    ">": "أ",
    "&": "ؤ",
    "<": "إ",
    "}": "ئ",
    "{": "ٱ",

    "A": "ا",
    "b": "ب",
    "p": "ة",
    "t": "ت",
    "v": "ث",
    "j": "ج",
    "H": "ح",
    "x": "خ",
    "d": "د",
    "*": "ذ",
    "r": "ر",
    "z": "ز",
    "s": "س",
    "$": "ش",
    "S": "ص",
    "D": "ض",
    "T": "ط",
    "Z": "ظ",
    "E": "ع",
    "g": "غ",
    "f": "ف",
    "q": "ق",
    "k": "ك",
    "l": "ل",
    "m": "م",
    "n": "ن",
    "h": "ه",
    "w": "و",
    "y": "ي",
    "Y": "ى",

    "a": "َ",
    "u": "ُ",
    "i": "ِ",
    "F": "ً",
    "N": "ٌ",
    "K": "ٍ",

    "~": "ّ",
    "o": "ْ",
    "`": "ٰ",
    "^": "ٓ",

    " ": " "
}


def bw_to_arabic(text):

    if not text:
        return ""

    result = []

    for char in text:
        result.append(
            BW_MAP.get(char, char)
        )

    return "".join(result)


def parse_features(features):

    result = {}

    for part in features.split("|"):

        part = part.strip()

        if not part:
            continue

        if ":" in part:

            key, value = part.split(
                ":",
                1
            )

            result[key] = value

        else:

            result[part] = True

    return result


def get_case(features):

    if "|GEN" in features or features.endswith("GEN"):
        return "GEN"

    if "|ACC" in features or features.endswith("ACC"):
        return "ACC"

    if "|NOM" in features or features.endswith("NOM"):
        return "NOM"

    if "|JUS" in features or features.endswith("JUS"):
        return "JUS"

    if "|SUBJ" in features or features.endswith("SUBJ"):
        return "SUBJ"

    if "|SUB" in features or features.endswith("SUB"):
        return "SUB"

    return ""


def get_feature(parsed, names):

    for name in names:

        if name in parsed:
            value = parsed[name]

            if value is True:
                return name

            return value

    return ""


def extract_morphology(parsed, features):

    result = {}

    # -------------------------
    # Aspect
    # -------------------------
    aspect = get_feature(
        parsed,
        ["PERF", "IMPF", "IMPV"]
    )

    if aspect:
        result["aspect"] = aspect


    # -------------------------
    # Mood
    # -------------------------
    mood = get_feature(
        parsed,
        ["IND", "SUBJ", "JUS", "SUB"]
    )

    # QAC: IMPF without explicit mood = indicative
    if not mood and aspect == "IMPF":
        mood = "IND"

    if mood:
        result["mood"] = mood


    # -------------------------
    # Voice
    # -------------------------
    voice = get_feature(
        parsed,
        ["ACT", "PASS"]
    )

    # QAC: active voice is the default
    if not voice:
        voice = "ACT"

    if voice:
        result["voice"] = voice


    # -------------------------
    # Verb Form
    # -------------------------
    form = parsed.get("FORM", "")

    # Source uses (IV), (X), (II), etc.
    if not form:
        match = re.search(
            r"\(([IVX]+)\)",
            features
        )

        if match:
            form = match.group(1)

    if form:
        result["form"] = form


    # -------------------------
    # Person / Gender / Number
    # -------------------------
    pgn = parsed.get("PERS", "")

    if not pgn:
        pgn = parsed.get("PGN", "")

    if not pgn:
        match = re.search(
            r"(?<![A-Z])([123])([MFD])?([SPD])(?=$|\|)",
            features
        )

        if match:
            pgn = match.group(0)

    if pgn:

        result["person_gender_number"] = pgn

        match = re.match(
            r"^([123])([MFD])?([SPD])$",
            pgn
        )

        if match:

            result["person"] = match.group(1)

            if match.group(2):
                result["gender"] = match.group(2)

            result["number"] = match.group(3)


    # -------------------------
    # Derivation
    # -------------------------
    derivation = get_feature(
        parsed,
        ["ACT PCPL", "PASS PCPL", "VN"]
    )

    if derivation:
        result["derivation"] = derivation


    return result


def load_quran_uthmani():

    ayahs = {}

    with open(
        QURAN_FILE,
        "r",
        encoding="utf-8-sig"
    ) as f:

        for ayah_number, line in enumerate(
            f,
            start=1
        ):

            line = line.strip()

            if not line:
                continue

            ayahs[ayah_number] = line

    return ayahs


def split_quran_words(text):

    return text.split()

def build_quran_word_map(quran_ayahs):

    word_map = {}

    global_ayah_number = 1

    for surah_number, ayah_count in enumerate(
        SURAH_AYAH_COUNTS,
        start=1
    ):

        for ayah_number in range(
            1,
            ayah_count + 1
        ):

            ayah_text = quran_ayahs[
                global_ayah_number
            ]

            words = split_quran_words(
                ayah_text
            )

            for word_number, word_text in enumerate(
                words,
                start=1
            ):

                key = (
                    f"{surah_number}:"
                    f"{ayah_number}:"
                    f"{word_number}"
                )

                word_map[key] = word_text

            global_ayah_number += 1

    return word_map
def parse_morphology(quran_words):

    records = {}
    print(
        "DEBUG INSIDE PARSER:",
        len(quran_words),
        repr(quran_words.get("2:3:2"))
    )
    with open(
        SOURCE_FILE,
        "r",
        encoding="utf-8-sig"
    ) as f:

        for line in f:

            line = line.rstrip("\n\r")

            if not line:
                continue

            if line.startswith("LOCATION"):
                continue

            parts = line.split("\t")

            if len(parts) != 4:
                continue

            location = parts[0]
            form = parts[1]
            tag = parts[2]
            features = parts[3]

            match = re.match(
                r"\((\d+):(\d+):(\d+):(\d+)\)",
                location
            )

            if not match:
                continue

            surah = int(match.group(1))
            ayah = int(match.group(2))
            word = int(match.group(3))
            segment = int(match.group(4))

            key = f"{surah}:{ayah}:{word}"

            parsed = parse_features(features)

            segment_type = ""

            if "PREFIX" in features:
                segment_type = "PREFIX"

            elif "STEM" in features:
                segment_type = "STEM"

            elif "SUFFIX" in features:
                segment_type = "SUFFIX"

            else:
                continue

            root_bw = parsed.get(
                "ROOT",
                ""
            )

            lemma_bw = parsed.get(
                "LEM",
                ""
            )

            if segment_type == "STEM" and tag == "V":
                morphology_features = extract_morphology(
                    parsed,
                    features
                )
            else:
                morphology_features = {}
            # Attached pronoun suffix
            # Example: PRON:3MP

            if segment_type == "SUFFIX" and tag == "PRON":

                pron_match = re.search(
                    r"PRON:(\d)([MF]?)([SDP]?)",
                    features
                )

                if pron_match:

                    pron_person = pron_match.group(1)
                    pron_gender = pron_match.group(2)
                    pron_number = pron_match.group(3)

                    morphology_features = {
                        "person": pron_person,
                        "gender": pron_gender,
                        "number": pron_number
                    }

                else:

                    morphology_features = {}
            if key == "2:3:2":
                print(
                    "DEBUG PARSE KEY =",
                    repr(key),
                    "QURAN VALUE =",
                    repr(quran_words.get(key))
                )
            if key not in records:

                records[key] = {
                    "surah": surah,
                    "ayah": ayah,
                    "word": word,
                    "text": quran_words.get(key, ""),
                    "segments": [],
                    "root": "",
                    "lemma": "",
                    "pos": "",
                    "case": "",
                    "features": {}
                }

            segment_data = {

                "segment": segment,

                "type": segment_type,

                "source_form": form,
                
                "source_form_ar": bw_to_arabic(form),

                "pos": tag,

                "root": bw_to_arabic(root_bw),

                "lemma": bw_to_arabic(lemma_bw),

                "case": get_case(features),

                "features": morphology_features
            }

            records[key]["segments"].append(
                segment_data
            )

            if segment_type == "STEM":

                records[key]["root"] = \
                    bw_to_arabic(root_bw)

                records[key]["lemma"] = \
                    bw_to_arabic(lemma_bw)

                records[key]["pos"] = tag

                records[key]["case"] = \
                    get_case(features)

                records[key]["features"] = \
                    morphology_features


    for key, record in records.items():

        arabic_word = record.get(
            "text",
            ""
        )
        if key == "2:3:2":
            print("DEBUG ARABIC WORD =", arabic_word)
        if arabic_word:

            record["segments"] = \
                split_arabic_word_by_segments(
                    arabic_word,
                    record["segments"]
                )


    return records

def main():

    print("======================================")
    print("Quran Morphology Converter")
    print("======================================")
    print()

    print("Loading Quran text...")
    
    quran_ayahs = load_quran_uthmani()

    print(
        f"Loaded {len(quran_ayahs)} ayahs."
    )
    quran_words = build_quran_word_map(
        quran_ayahs
    )
    print(
        "TEST 2:3:2 =",
        repr(quran_words.get("2:3:2"))
    )
    print(
        f"Mapped {len(quran_words)} Quran words."
    )
    print()

    print("Loading morphology source...")

    morphology = parse_morphology(
        quran_words
    )
    print(
        f"Loaded {len(morphology)} word records."
    )

    print()

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    # --------------------------------------
    # Standard Quran ayah counts
    # --------------------------------------

    ayah_counts = [
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


    # --------------------------------------
    # Build surah/ayah → Quran text mapping
    # --------------------------------------

    global_ayah = 1

    ayah_text = {}

    for surah_number, count in enumerate(
        ayah_counts,
        start=1
    ):

        for ayah_number in range(
            1,
            count + 1
        ):

            ayah_text[
                (surah_number, ayah_number)
            ] = quran_ayahs.get(
                global_ayah,
                ""
            )

            global_ayah += 1


    # --------------------------------------
    # Generate morphology files
    # --------------------------------------

    surah_data = {}

    matched = 0
    missing = 0

    for record_key, record in morphology.items():

        surah = record["surah"]
        ayah = record["ayah"]
        word_index = record["word"]

        text = ayah_text.get(
            (surah, ayah),
            ""
        )

        words = split_quran_words(text)

        if word_index > len(words):

            missing += 1

            continue

        arabic_word = words[
            word_index - 1
        ]


        if surah not in surah_data:

            surah_data[surah] = {

                "metadata": {

                    "surah": surah,

                    "source": (
                        "Quranic Arabic Corpus v0.4 / "
                        "mustafa0x/quran-morphology"
                    ),

                    "quran_text_source": (
                        "quran-uthmani.txt"
                    ),

                    "purpose": (
                        "Word-level morphology"
                    )
                },

                "words": {}
            }

        if record_key == "2:3:2":
            print(
                "DEBUG BEFORE JSON:",
                record["segments"]
            )
        word_data = {

    "text": arabic_word,

    "root": record["root"],

    "lemma": record["lemma"],

    "pos": record["pos"],

    "case": record["case"],

    "segments": record["segments"]
}


        # Add detailed morphology
        # only when available.

        for key, value in record["features"].items():

            if value:
                word_data[key] = value


        surah_data[surah]["words"][
            record_key
        ] = word_data


        matched += 1


    print(
        f"Matched words: {matched}"
    )

    print(
        f"Missing words: {missing}"
    )

    print()


    # --------------------------------------
    # Write 114 JSON files
    # --------------------------------------

    for surah in range(1, 115):

        output_file = os.path.join(
            OUTPUT_DIR,
            f"{surah}.json"
        )

        data = surah_data.get(
            surah,
            {
                "metadata": {
                    "surah": surah,
                    "purpose": (
                        "Word-level morphology"
                    )
                },
                "words": {}
            }
        )


        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )


        print(
            f"Created morphology\\{surah}.json"
        )

    
    print()
    print("======================================")
    print("Conversion completed.")
    print("======================================")

def split_arabic_word_by_segments(
    arabic_word,
    segments
):
    """
    Qur'an-এর আসল Arabic word থেকে
    morphology segment অনুযায়ী অংশ আলাদা করে।

    Qur'anic combining marks অক্ষুণ্ণ রাখা হয়।
    """

    import unicodedata

    def normalize_arabic(text):

        replacements = {
            "ی": "ي",
            "ى": "ي",
            "ک": "ك",
            "ٱ": "ا",
            "أ": "ا",
            "إ": "ا",
            "آ": "ا"
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        result = ""

        for char in text:

            if unicodedata.category(char) in (
                "Mn",
                "Me"
            ):
                continue

            result += char

        return result

    def get_base_characters(text):

        clusters = []

        current = ""

        for char in text:

            if unicodedata.category(char) in (
                "Mn",
                "Me"
            ):

                current += char

            else:

                if current:
                    clusters.append(current)

                current = char

        if current:
            clusters.append(current)

        return clusters

    # Qur'an-এর আসল word-কে
    # base character + তার marks অনুযায়ী ভাগ করা
    word_clusters = get_base_characters(
        arabic_word
    )

    # matching-এর জন্য শুধু base characters ব্যবহার করা
    normalized_word = normalize_arabic(
        arabic_word
    )

    result = []

    position = 0

    for segment in segments:

        source_form_ar = segment.get(
            "source_form_ar",
            ""
        )

        normalized_segment = normalize_arabic(
            source_form_ar
        )

        if not normalized_segment:

            result.append(segment)

            continue

        start = normalized_word.find(
            normalized_segment,
            position
        )

        if start == -1:

            print(
                "WARNING: segment not matched:",
                arabic_word,
                source_form_ar
            )

            result.append(segment)

            continue

        end = start + len(
            normalized_segment
        )

        segment_copy = dict(segment)

        # এখানে morphology source নয়,
        # Qur'an-এর আসল word থেকে অংশ নেওয়া হচ্ছে
        segment_copy["source_form_ar"] = "".join(
            word_clusters[start:end]
        )

        result.append(segment_copy)

        position = end

    return result
    

if __name__ == "__main__":
    main()
