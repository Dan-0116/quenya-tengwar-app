import streamlit as st

# =========================================================
# Streamlit 기본 설정 (반드시 최상단)
# =========================================================

st.set_page_config(page_title="한국어 → 퀘냐 텡과르 번역기")

# =========================================================
# 폰트 로딩 (CSS)
# =========================================================

st.markdown("""
<style>
@font-face {
    font-family: 'Tengwar';
    src: url('./TengwarAnnatar.ttf') format('truetype');
}
.tengwar {
    font-family: 'Tengwar';
    font-size: 40px;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 1. 한글 음절 분해
# =========================================================

CHOSUNG = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
JUNGSUNG = ["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"]
JONGSUNG = ["","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]

def decompose(char):
    if not "가" <= char <= "힣":
        return char, "", ""
    code = ord(char) - 0xAC00
    return (
        CHOSUNG[code // 588],
        JUNGSUNG[(code % 588) // 28],
        JONGSUNG[code % 28]
    )

# =========================================================
# 2. 자음 → 테마르 / 텔레르
# =========================================================

CONSONANT_FEATURE_MAP = {
    "ㄱ": ("CALMA", 1), "ㄲ": ("CALMA", 1), "ㅋ": ("CALMA", 1),
    "ㄴ": ("TINCO", 5),
    "ㄷ": ("TINCO", 1), "ㅌ": ("TINCO", 1),
    "ㄹ": ("TINCO", 6),
    "ㅁ": ("PARMA", 5),
    "ㅂ": ("PARMA", 1), "ㅍ": ("PARMA", 1),
    "ㅅ": ("TINCO", 3),
    "ㅇ": ("CALMA", 5),
    "ㅎ": ("CALMA", 3),
    "ㅈ": ("TINCO", 2),
    "ㅊ": ("TINCO", 1)
}

# =========================================================
# 3. 텡과르 글리프
# =========================================================

TENGWAR_GLYPH = {
    ("TINCO", 1): "\ue000",
    ("TINCO", 2): "\ue001",
    ("TINCO", 3): "\ue002",
    ("TINCO", 5): "\ue004",
    ("TINCO", 6): "\ue005",
    ("PARMA", 1): "\ue010",
    ("PARMA", 5): "\ue014",
    ("CALMA", 1): "\ue020",
    ("CALMA", 3): "\ue022",
    ("CALMA", 5): "\ue024"
}

# =========================================================
# 4. 테흐타 (모음)
# =========================================================

VOWEL_TEHTA = {
    "ㅏ": "\ue040",
    "ㅓ": "\ue041",
    "ㅣ": "\ue042",
    "ㅗ": "\ue043",
    "ㅜ": "\ue044",
    "ㅡ": "\ue045"
}

# =========================================================
# 5. 변환 로직
# =========================================================

def hangul_to_tengwar(text):
    output = ""
    for ch in text:
        if ch == " ":
            output += "   "
            continue

        cho, jung, jong = decompose(ch)

        if cho in CONSONANT_FEATURE_MAP:
            theme, grade = CONSONANT_FEATURE_MAP[cho]
            output += TENGWAR_GLYPH.get((theme, grade), "")

        if jung in VOWEL_TEHTA:
            output += VOWEL_TEHTA[jung]

        if jong in CONSONANT_FEATURE_MAP:
            theme, grade = CONSONANT_FEATURE_MAP[jong]
            output += TENGWAR_GLYPH.get((theme, grade), "")

        output += " "
    return output

# =========================================================
# 6. UI
# =========================================================

st.title("한국어 → 퀘냐 텡과르 번역기")
st.write("퀘냐 오마테흐타 · 실제 텡과르 문자 출력")

text = st.text_input("한국어 문장을 입력하세요")

if text:
    result = hangul_to_tengwar(text)
    st.subheader("퀘냐 텡과르 표기")
    st.markdown(f"<div class='tengwar'>{result}</div>", unsafe_allow_html=True)
