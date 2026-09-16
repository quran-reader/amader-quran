let quranData = {};
let translationData = {};
let rootData = {};
let surahMorphologyData = {};
let adminTranslations = {};
let currentSurah = 1;
let currentAyah = 1;
let currentMode = "reader";
let bookmarks =
    JSON.parse(localStorage.getItem("quranBookmarks")) || [];
const surahNames = {
    1: ["আল-ফাতিহা", "الفاتحة"],
    2: ["আল-বাকারা", "البقرة"],
    3: ["আলে ইমরান", "آل عمران"],
    4: ["আন-নিসা", "النساء"],
    5: ["আল-মায়িদাহ", "المائدة"],
    6: ["আল-আনআম", "الأنعام"],
    7: ["আল-আরাফ", "الأعراف"],
    8: ["আল-আনফাল", "الأنفال"],
    9: ["আত-তাওবা", "التوبة"],
    10: ["ইউনুস", "يونس"],
    11: ["হুদ", "هود"],
    12: ["ইউসুফ", "يوسف"],
    13: ["আর-রাদ", "الرعد"],
    14: ["ইবরাহিম", "إبراهيم"],
    15: ["আল-হিজর", "الحجر"],
    16: ["আন-নাহল", "النحل"],
    17: ["আল-ইসরা", "الإسراء"],
    18: ["আল-কাহফ", "الكهف"],
    19: ["মারইয়াম", "مريم"],
    20: ["ত্ব-হা", "طه"],
    21: ["আল-আম্বিয়া", "الأنبياء"],
    22: ["আল-হাজ্জ", "الحج"],
    23: ["আল-মুমিনুন", "المؤمنون"],
    24: ["আন-নূর", "النور"],
    25: ["আল-ফুরকান", "الفرقان"],
    26: ["আশ-শুআরা", "الشعراء"],
    27: ["আন-নামল", "النمل"],
    28: ["আল-কাসাস", "القصص"],
    29: ["আল-আনকাবুত", "العنكبوت"],
    30: ["আর-রূম", "الروم"],
    31: ["লুকমান", "لقمان"],
    32: ["আস-সাজদাহ", "السجدة"],
    33: ["আল-আহযাব", "الأحزاب"],
    34: ["সাবা", "سبأ"],
    35: ["ফাতির", "فاطر"],
    36: ["ইয়াসীন", "يس"],
    37: ["আস-সাফফাত", "الصافات"],
    38: ["সাদ", "ص"],
    39: ["আয-যুমার", "الزمر"],
    40: ["গাফির", "غافر"],
    41: ["ফুসসিলাত", "فصلت"],
    42: ["আশ-শূরা", "الشورى"],
    43: ["আয-যুখরুফ", "الزخرف"],
    44: ["আদ-দুখান", "الدخان"],
    45: ["আল-জাসিয়াহ", "الجاثية"],
    46: ["আল-আহকাফ", "الأحقاف"],
    47: ["মুহাম্মদ", "محمد"],
    48: ["আল-ফাতহ", "الفتح"],
    49: ["আল-হুজুরাত", "الحجرات"],
    50: ["কাফ", "ق"],
    51: ["আয-যারিয়াত", "الذاريات"],
    52: ["আত-তূর", "الطور"],
    53: ["আন-নাজম", "النجم"],
    54: ["আল-কামার", "القمر"],
    55: ["আর-রহমান", "الرحمن"],
    56: ["আল-ওয়াকিয়াহ", "الواقعة"],
    57: ["আল-হাদীদ", "الحديد"],
    58: ["আল-মুজাদালাহ", "المجادلة"],
    59: ["আল-হাশর", "الحشر"],
    60: ["আল-মুমতাহিনাহ", "الممتحنة"],
    61: ["আস-সাফ", "الصف"],
    62: ["আল-জুমুআহ", "الجمعة"],
    63: ["আল-মুনাফিকুন", "المنافقون"],
    64: ["আত-তাগাবুন", "التغابن"],
    65: ["আত-তালাক", "الطلاق"],
    66: ["আত-তাহরীম", "التحريم"],
    67: ["আল-মুলক", "الملك"],
    68: ["আল-কলম", "القلم"],
    69: ["আল-হাক্কাহ", "الحاقة"],
    70: ["আল-মাআরিজ", "المعارج"],
    71: ["নূহ", "نوح"],
    72: ["আল-জিন্ন", "الجن"],
    73: ["আল-মুযযাম্মিল", "المزمل"],
    74: ["আল-মুদ্দাসসির", "المدثر"],
    75: ["আল-কিয়ামাহ", "القيامة"],
    76: ["আল-ইনসান", "الإنسان"],
    77: ["আল-মুরসালাত", "المرسلات"],
    78: ["আন-নাবা", "النبأ"],
    79: ["আন-নাযিআত", "النازعات"],
    80: ["আবাসা", "عبس"],
    81: ["আত-তাকভীর", "التكوير"],
    82: ["আল-ইনফিতার", "الانفطار"],
    83: ["আল-মুতাফফিফীন", "المطففين"],
    84: ["আল-ইনশিকাক", "الانشقاق"],
    85: ["আল-বুরুজ", "البروج"],
    86: ["আত-তারিক", "الطارق"],
    87: ["আল-আলা", "الأعلى"],
    88: ["আল-গাশিয়াহ", "الغاشية"],
    89: ["আল-ফজর", "الفجر"],
    90: ["আল-বালাদ", "البلد"],
    91: ["আশ-শামস", "الشمس"],
    92: ["আল-লাইল", "الليل"],
    93: ["আদ-দুহা", "الضحى"],
    94: ["আশ-শরহ", "الشرح"],
    95: ["আত-তীন", "التين"],
    96: ["আল-আলাক", "العلق"],
    97: ["আল-কদর", "القدر"],
    98: ["আল-বাইয়্যিনাহ", "البينة"],
    99: ["আয-যিলযাল", "الزلزلة"],
    100: ["আল-আদিয়াত", "العاديات"],
    101: ["আল-কারিআহ", "القارعة"],
    102: ["আত-তাকাসুর", "التكاثر"],
    103: ["আল-আসর", "العصر"],
    104: ["আল-হুমাযাহ", "الهمزة"],
    105: ["আল-ফীল", "الفيل"],
    106: ["কুরাইশ", "قريش"],
    107: ["আল-মাউন", "الماعون"],
    108: ["আল-কাওসার", "الكوثر"],
    109: ["আল-কাফিরুন", "الكافرون"],
    110: ["আন-নাসর", "النصر"],
    111: ["আল-মাসাদ", "المسد"],
    112: ["আল-ইখলাস", "الإخلاص"],
    113: ["আল-ফালাক", "الفلق"],
    114: ["আন-নাস", "الناس"]
};

// -------------------------------------
// HTML elements
// -------------------------------------

const surahSelect =
    document.getElementById("surahSelect");
const readerModeButton = document.getElementById("readerModeButton");
const adminModeButton = document.getElementById("adminModeButton");
const currentModeDisplay =
    document.getElementById("currentModeDisplay");
const adminLogoutButton =
    document.getElementById("adminLogoutButton");
const surahTitle =
    document.getElementById("surahTitle");

const ayahContainer =
    document.getElementById("ayahContainer");

const wordAnalysis =
    document.getElementById("wordAnalysis");

const prevAyah =
    document.getElementById("prevAyah");

const nextAyah =
    document.getElementById("nextAyah");
const bookmarkAyah = document.getElementById("bookmarkButton");
const bookmarkList = document.getElementById("bookmarkList");
// -------------------------------------
// Load Quran
// -------------------------------------
async function loadAdminTranslations() {

    try {

        const response =
            await fetch(
                "https://amader-quran-backend.onrender.com/api/translations"
            );

        if (!response.ok) {

            throw new Error(
                "Admin translations could not be loaded."
            );

        }

        adminTranslations =
            await response.json();

        console.log(
            "Online admin translations loaded:",
            adminTranslations
        );

    } catch (error) {

        console.error(
            "Admin translation loading error:",
            error
        );

    }
}
async function loadQuran() {
    await loadAdminTranslations();
    try {

        console.log("Quran application starting...");


        // Quran
        const quranResponse =
            await fetch("./data/quran.json");

        if (!quranResponse.ok) {
            throw new Error(
                "Quran data could not be loaded."
            );
        }

        quranData =
            await quranResponse.json();


        // Bangla translation
        const translationResponse =
            await fetch("./data/translation_bn.json");

        if (!translationResponse.ok) {
            throw new Error(
                "Bangla translation could not be loaded."
            );
        }

        translationData =
            await translationResponse.json();


        // Root database
        const rootResponse =
            await fetch("./data/roots.json");

        if (!rootResponse.ok) {
            throw new Error(
                "Root data could not be loaded."
            );
        }

        rootData =
            await rootResponse.json();


        console.log("Quran loaded.");
        console.log("Translation loaded.");
        console.log("Root database loaded.");


        // প্রথম সূরা
        loadSurah(1);


    } catch (error) {

        console.error(
            "Quran App Error:",
            error
        );

        ayahContainer.innerHTML = `
            <div class="ayah">
                <strong>Quran data loading error.</strong>
                <br><br>
                ${error.message}
            </div>
        `;
    }
}


// -------------------------------------
// Load Surah
// -------------------------------------
async function loadSurahMorphology(surahNumber) {

    try {

        const response =
            await fetch(
                `./data/morphology/${surahNumber}.json`
            );

        if (!response.ok) {
            throw new Error(
                "Morphology file could not be loaded."
            );
        }

        surahMorphologyData =
            await response.json();

        console.log(
            `Surah ${surahNumber} morphology loaded.`
        );

    } catch (error) {

        console.error(
            "Morphology loading error:",
            error
        );

        surahMorphologyData = {};
    }
}
function loadSurah(surahNumber, ayahNumber = 1) {

    currentSurah =
        Number(surahNumber);

    currentAyah = Number(ayahNumber);

 
    const surah =
        quranData[currentSurah];


    if (!surah) {

        console.error(
            "Surah not found:",
            currentSurah
        );

        return;
    }


    const names = surahNames[currentSurah];

    surahTitle.textContent =
        `সূরা ${currentSurah} — ${names[0]} (${names[1]})`;


    showSingleAyah(
    surah.ayahs[currentAyah - 1]
);
}


// -------------------------------------
// Surah selection
// -------------------------------------

surahSelect.addEventListener(
    "change",
    function () {

        loadSurah(
            this.value
        );

    }
);


// -------------------------------------
// Show single Ayah
// -------------------------------------

function showSingleAyah(ayah) {

    ayahContainer.innerHTML = "";


    const ayahElement =
        document.createElement("div");


    ayahElement.className =
        "ayah";


    const translationAyahs =
    translationData[currentSurah]?.ayahs;

let translation = "";

const centralTranslation =
    adminTranslations[currentSurah]?.[ayah.number];

const savedTranslation =
    localStorage.getItem(
        `translation_${currentSurah}_${ayah.number}`
    );

if (centralTranslation) {

    translation = centralTranslation;

} else if (savedTranslation !== null) {

    translation = savedTranslation;

}
if (savedTranslation !== null) {

    translation = savedTranslation;

} else if (Array.isArray(translationAyahs)) {

    const translationAyah =
        translationAyahs.find(
            item => Number(item.number) === Number(ayah.number)
        );

    translation =
        translationAyah?.translation || "";

} else if (translationAyahs) {

    const translationItem =
        translationAyahs[String(ayah.number)];

    if (typeof translationItem === "string") {

        translation = translationItem;

    } else {

        translation =
            translationItem?.translation || "";
    }
}


    ayahElement.innerHTML = `
        <div class="ayah-number">
            আয়াত ${ayah.number}
        </div>
        <div
            class="arabic"
            data-ayah="${ayah.number}"
        >
            ${ayah.text
                .split(" ")
                .map(
                    word =>
                        `<span class="quran-word">
                            ${word}
                        </span>`
                )
                .join(" ")
            }
        </div>
        <div class="translation-bn">
            ${translation}
        </div>
        <button id="editTranslationButton">
            ✏️ অনুবাদ সংশোধন
        </button>
    `;


    ayahContainer.appendChild(
        ayahElement
    );
    const editBox = document.createElement("textarea");

editBox.id = "translationEditBox";

editBox.value = translation;

editBox.style.width = "100%";
editBox.style.minHeight = "120px";
editBox.style.marginTop = "10px";
editBox.style.display = "none";

ayahElement.appendChild(editBox);
  const saveButton = document.createElement("button");

saveButton.textContent = "💾 সংরক্ষণ";

const cancelButton = document.createElement("button");

cancelButton.textContent = "↩️ বাতিল";
saveButton.style.display = "none";
cancelButton.style.display = "none";
editBox.after(saveButton, cancelButton);
  saveButton.addEventListener("click", function () {
      if (editBox.value.trim() === "") {

          alert("⚠️ অনুবাদ খালি রাখা যাবে না।");

          return;
      }
    translation = editBox.value;

    localStorage.setItem(
        `translation_${currentSurah}_${ayah.number}`,
        translation
    );
    fetch("https://amader-quran-backend.onrender.com/api/translations", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            surah: currentSurah,
            ayah: ayah.number,
            translation: translation
       })
})
.then(response => response.json())
.then(data => {

    if (!data.success) {
        throw new Error(data.message || "Translation save failed.");
    }

    console.log("✅ Central translation saved:", data);

})
.catch(error => {

    console.error(
        "❌ Central translation save error:",
        error
    );

});
    ayahElement.querySelector(".translation-bn").textContent = translation;
    editBox.style.display = "none";
    saveButton.style.display = "none";
    cancelButton.style.display = "none";

    alert("✅ অনুবাদ সংরক্ষণ করা হয়েছে।");

});
  cancelButton.addEventListener("click", function () {

    editBox.value = translation;

    editBox.style.display = "none";
    saveButton.style.display = "none";
    cancelButton.style.display = "none";

});
  const resetButton = document.createElement("button");

resetButton.textContent = "↩️ মূল অনুবাদে ফিরুন";

resetButton.style.display = "none";

cancelButton.after(resetButton);

resetButton.addEventListener("click", function () {

    localStorage.removeItem(
        `translation_${currentSurah}_${ayah.number}`
    );

    loadSurah(currentSurah, ayah.number);

    alert("↩️ মূল অনুবাদে ফিরিয়ে দেওয়া হয়েছে।");

});
const editTranslationButton =
    document.getElementById("editTranslationButton");

if (currentMode === "reader") {

    editTranslationButton.style.display = "none";
    resetButton.style.display = "none";

} else {

    editTranslationButton.style.display = "inline-block";
    resetButton.style.display = "inline-block";

}

editTranslationButton.addEventListener("click", function () {

    editBox.style.display = "block";
    saveButton.style.display = "inline-block";
    cancelButton.style.display = "inline-block";

});
    activateWordSelection();

    updateNavigationButtons();
}


// -------------------------------------
// Word selection
// -------------------------------------

function activateWordSelection() {

    document
        .querySelectorAll(".quran-word")
        .forEach(
            function (element) {

                element.addEventListener(
                    "click",
                    function () {

                        const selectedText =
                            this.textContent.trim();


                        showWordAnalysis(
                            selectedText
                        );

                    }
                );

            }
        );
}


// -------------------------------------
// Word analysis
// -------------------------------------

function showWordAnalysis(selectedText) {

    const cleanWord =
        selectedText.replace(
            /[ۖۗۚۛۙۜۘ۝۞]/g,
            ""
        );

    const wordInfo =
        rootData[cleanWord];

    if (!wordInfo) {

        wordAnalysis.innerHTML = `
            <h3>শব্দ বিশ্লেষণ</h3>
            <div class="selected-word">
                ${selectedText}
            </div>
            <p>
                এই শব্দের তথ্য এখনো
                database-এ যুক্ত করা হয়নি।
            </p>
        `;

        return;
    }

    wordAnalysis.innerHTML = `
        <h3>শব্দ বিশ্লেষণ</h3>
        <div class="selected-word">
            ${selectedText}
        </div>
        <p>
            <strong>Root:</strong>
            ${wordInfo.root || ""}
        </p>
        <p>
            <strong>মূল রূপ:</strong>
            ${wordInfo.form || ""}
        </p>
        <p>
            <strong>শব্দের ধরন:</strong>
            ${wordInfo.type || ""}
        </p>
        <p>
            <strong>আভিধানিক প্রাসঙ্গিক অর্থ:</strong>
            ${wordInfo.meaning_bn || ""}
        </p>
    `;
}

// -------------------------------------
// Previous Ayah
// -------------------------------------

prevAyah.addEventListener(
    "click",
    function () {

        if (currentAyah > 1) {

            currentAyah--;

            const ayah =
                quranData[currentSurah]
                    .ayahs[currentAyah - 1];

            showSingleAyah(
                ayah
            );
        }

    }
);


// -------------------------------------
// Next Ayah
// -------------------------------------

nextAyah.addEventListener(
    "click",
    function () {

        const ayahs =
            quranData[currentSurah]
                ?.ayahs;


        if (!ayahs) {
            return;
        }


        if (
            currentAyah <
            ayahs.length
        ) {

            currentAyah++;

            const ayah =
                ayahs[currentAyah - 1];

            showSingleAyah(
                ayah
            );
        }

    }
);


// -------------------------------------
// Navigation buttons
// -------------------------------------

function updateNavigationButtons() {

    const ayahs =
        quranData[currentSurah]
            ?.ayahs;


    if (!ayahs) {
        return;
    }


    prevAyah.disabled =
        currentAyah <= 1;


    nextAyah.disabled =
        currentAyah >= ayahs.length;
}


// -------------------------------------
// Bookmark
// -------------------------------------



// -------------------------------------
// Search
// -------------------------------------

document
    .getElementById("searchButton")
    .addEventListener(
        "click",
        function () {

            alert(
                "Search system পরবর্তী ধাপে যুক্ত হবে।"
            );

        }
    );

function showBookmarks() {

    bookmarkList.innerHTML = "";

    bookmarks.forEach(function (item) {

        const div = document.createElement("div");

        div.textContent =
            `🔖 সূরা ${item.surah}, আয়াত ${item.ayah}`;

        div.style.cursor = "pointer";

        div.addEventListener("click", function () {

    currentSurah = item.surah;
    currentAyah = item.ayah;

    loadSurah(currentSurah);

});

const removeButton = document.createElement("button");

removeButton.textContent = "❌ মুছুন";

removeButton.addEventListener("click", function (event) {

    event.stopPropagation();

    bookmarks = bookmarks.filter(function (bookmark) {

        return !(
            bookmark.surah === item.surah &&
            bookmark.ayah === item.ayah
        );

    });

    localStorage.setItem(
        "quranBookmarks",
        JSON.stringify(bookmarks)
    );

    showBookmarks();

});

div.appendChild(removeButton);

bookmarkList.appendChild(div);

    });

}
// -------------------------------------
// Start application
// -------------------------------------

bookmarkAyah.addEventListener("click", function () {

    const alreadyBookmarked = bookmarks.some(
    item =>
        item.surah === currentSurah &&
        item.ayah === currentAyah
);

if (alreadyBookmarked) {
    alert("🔖 এই আয়াতটি ইতিমধ্যেই Bookmark করা আছে।");
    return;
}

bookmarks.push({
    surah: currentSurah,
    ayah: currentAyah
});
    localStorage.setItem("quranBookmarks", JSON.stringify(bookmarks));
    showBookmarks();
    alert("🔖 আয়াতটি Bookmark করা হয়েছে।");

});
loadQuran();
showBookmarks();
readerModeButton.addEventListener("click", function () {

    currentMode = "reader";
    currentModeDisplay.textContent = "👤 সাধারণ Reader Mode";
    adminLogoutButton.style.display =
        "none";

    adminModeButton.style.display =
        "inline-block";
    loadSurah(currentSurah);

    alert("👤 সাধারণ Reader Mode চালু হয়েছে।");

});


adminModeButton.addEventListener("click", async function () {

    const password = prompt("🔐 Admin Password দিন:");

    if (!password) {
        return;
    }

    try {

        const response = await fetch(
            "https://amader-quran-backend.onrender.com/api/admin/login",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    password: password
                })
            }
        );

        const data = await response.json();

        if (data.success) {

            currentMode = "admin";

            currentModeDisplay.textContent =
                "👨‍💼 Admin Mode";

            adminLogoutButton.style.display =
                "inline-block";

            adminModeButton.style.display =
                "none";

            loadSurah(currentSurah);

            alert("👨‍💼 Admin Mode চালু হয়েছে।");

        } else {

            currentMode = "reader";

            alert("❌ Password সঠিক নয়।");

        }

    } catch (error) {

        console.error(
            "❌ Admin login error:",
            error
        );

        alert(
            "⚠️ Server-এর সাথে যোগাযোগ করা যাচ্ছে না।"
        );

    }

});
adminLogoutButton.addEventListener("click", function () {

    currentMode = "reader";

    currentModeDisplay.textContent =
        "👤 সাধারণ Reader Mode";

    adminLogoutButton.style.display = "none";
    adminModeButton.style.display =
    "inline-block";
    loadSurah(currentSurah);

    alert("🚪 Admin Logout হয়েছে।");

});