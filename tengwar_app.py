import streamlit as st

# =========================================================
# 1. 한글 음절 분해
# =========================================================

CHOSUNG = [
    "ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ",
    "ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"
]

JUNGSUNG = [
    "ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ",
    "ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"
]

JONGSUNG = [
    "","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ",
    "ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ",
    "ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"
]

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
# 2. 퀘냐식 자음 → Annatar 키보드 매핑
# =========================================================

TENGWAR_CONSONANT = {
    "ㄱ": "k", "ㄲ": "k", "ㅋ": "k",
    "ㄴ": "n",
    "ㄷ": "t", "ㅌ": "t",
    "ㄹ": "r",
    "ㅁ": "m",
    "ㅂ": "p", "ㅍ": "p",
    "ㅅ": "s",
    "ㅇ": "g",
    "ㅎ": "h",
    "ㅈ": "j",
    "ㅊ": "c"
}

# =========================================================
# 3. 모음 (Annatar 키보드 입력)
# =========================================================

TENGWAR_VOWEL = {
    "ㅏ": "a",
    "ㅓ": "e",
    "ㅣ": "i",
    "ㅗ": "o",
    "ㅜ": "u",
    "ㅡ": "ë"
}

# =========================================================
# 4. 변환 로직
# =========================================================

def hangul_to_tengwar(text):
    result = ""
    for ch in text:
        if ch == " ":
            result += "   "
            continue

        cho, jung, jong = decompose(ch)

        if cho in TENGWAR_CONSONANT:
            result += TENGWAR_CONSONANT[cho]

        if jung in TENGWAR_VOWEL:
            result += TENGWAR_VOWEL[jung]

        if jong in TENGWAR_CONSONANT:
            result += TENGWAR_CONSONANT[jong]

        result += " "

    return result

# =========================================================
# 5. Streamlit UI
# =========================================================

st.set_page_config(page_title="한국어 → 퀘냐 텡과르 번역기")

st.markdown("""
<style>
.tengwar {
    font-family: 'Tengwar Annatar', 'Tengwar', serif;
    font-size: 42px;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

st.title("한국어 → 퀘냐 텡과르 번역기")
st.write("Tengwar Annatar (키보드 매핑 방식) · 실제 문자 출력")

text = st.text_input("한국어 문장을 입력하세요")

if text:
    output = hangul_to_tengwar(text)
    st.subheader("퀘냐식 텡과르 표기")
    st.markdown(f"<div class='tengwar'>{output}</div>", unsafe_allow_html=True)

st.subheader("폰트 테스트")
st.markdown(
    "<div class='tengwar'>tengwar annatar test</div>",
    unsafe_allow_html=True
)
