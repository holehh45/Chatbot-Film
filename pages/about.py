import streamlit as st

st.set_page_config(
    page_title="Tentang MovieBot",
    page_icon="ℹ️"
)

st.title("ℹ️ Tentang MovieBot")

if st.button("⬅ Kembali ke Dashboard"):
    st.switch_page("app.py")

st.markdown("""
## MovieBot

MovieBot adalah chatbot rekomendasi film yang
dibangun menggunakan:

- Python
- Streamlit
- Finite State Machine (FSM)
- Regular Expression

### Mata Kuliah

Teori Bahasa dan Otomata

### Tujuan

Mengimplementasikan konsep FSM dalam sistem chatbot
untuk membantu pengguna menemukan rekomendasi film.
""")