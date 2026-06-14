import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Rekomendasi Film",
    page_icon="🎥"
)

st.title("🎥 Daftar Film")

if st.button("⬅ Kembali ke Dashboard"):
    st.switch_page("app.py")

movies = pd.read_csv("data/movies.csv")

genre = st.selectbox(
    "Pilih Genre",
    sorted(movies["genre"].unique())
)

filtered = movies[
    movies["genre"] == genre
]

for _, movie in filtered.iterrows():

    with st.container(border=True):

        col1, col2 = st.columns([1, 3])

        with col1:

            st.image(
                movie["poster"],
                width="stretch"
            )

        with col2:

            st.subheader(movie["title"])

            st.write(
                f"🎭 {movie['genre']}"
            )

            st.write(
                f"⭐ {movie['rating']}"
            )

            st.write(
                f"📅 {movie['year']}"
            )

            if st.button(
                f"Detail {movie['title']}",
                key=movie["title"],
                width="stretch"
            ):
                st.session_state.selected_movie = movie["title"]