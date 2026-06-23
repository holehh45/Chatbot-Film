import streamlit as st

st.set_page_config(
page_title="Tentang MovieBot",
page_icon="🎬",
layout="wide"
)

# header

col1, col2 = st.columns([8, 1])

with col2:
    if st.button("🏠 Dashboard"):
        st.switch_page("app.py")

st.header(
"🎬 Tentang MovieBot",
divider="rainbow"
)

# hero section

st.markdown("""

# 🍿 MovieBot

### Chatbot Rekomendasi Film Berbasis Finite State Machine (FSM)

MovieBot membantu pengguna menemukan film berdasarkan genre,
melihat detail film, serta mendapatkan rekomendasi film serupa
melalui percakapan yang interaktif dan natural.
""")

st.divider()

# FITUR

st.subheader("✨ Fitur Utama")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""

### 🎬 Rekomendasi Film

Memberikan rekomendasi film berdasarkan genre yang dipilih pengguna.
""")

with col2:
    st.info("""

### 📖 Detail Film

Menampilkan informasi film seperti genre, tahun, rating, poster, dan sinopsis.
""")

with col3:
    st.info("""

### 🤖 Percakapan Natural

Mendukung pertanyaan lanjutan seperti:

* ratingnya berapa?
* genrenya apa?
* film serupa
  """)

st.divider()

# teknologi

st.subheader("🛠️ Teknologi yang Digunakan")

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:
    st.metric(
"Python",
"3.x"
)

with tech2:
    st.metric(
"Framework",
"Streamlit"
)

with tech3:
    st.metric(
"Engine",
"FSM"
)

with tech4:
    st.metric(
"Parsing",
"Regex"
)

st.divider()

# FSM

st.subheader("🔄 Arsitektur Finite State Machine")

st.code("""
START
↓
MAIN_MENU
↓
RECOMMENDATION
↓
DETAIL
↓
MAIN_MENU
""")

st.success("""
FSM digunakan untuk mengatur alur percakapan sehingga chatbot
dapat memahami konteks dan memberikan respons yang sesuai.
""")

st.divider()
