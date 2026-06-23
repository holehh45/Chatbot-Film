import streamlit as st
import pandas as pd

from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(
    page_title="MovieBot",
    page_icon="🎬",
    layout="wide"
)

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# dataset

movies = pd.read_csv("data/movies.csv")

# hero section

st.markdown("""
<div class='hero-card'>

# 🎬 MovieBot

Temukan film favoritmu dengan chatbot rekomendasi film.

🤖 Chatbot Film  
🎭 Rekomendasi Genre  
📖 Detail Film

</div>
""", unsafe_allow_html=True)

st.markdown("### Temukan film favoritmu dengan bantuan chatbot pintar")

hero_movie = movies.sort_values(
    by="rating",
    ascending=False
).iloc[0]

st.container(border=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.image(
        hero_movie["poster"],
        width="stretch"
    )

with col2:

    st.title(hero_movie["title"])

    st.write(
        f"⭐ {hero_movie['rating']}"
    )

    st.write(
        f"🎭 {hero_movie['genre']}"
    )

    st.write(
        "Film pilihan terbaik minggu ini."
    )

    if st.button(
        "🎬 Mulai Chat",
        type="primary",
        width="stretch"
    ):
        st.switch_page(
            "pages/chatbot.py"
        )

# navigation

st.markdown("---")

c1, c2, c3 = st.columns(3)

with c1:

    if st.button(
        "🤖 Mulai Chatbot",
        width="stretch"
    ):
        st.switch_page("pages/chatbot.py")

with c2:

    if st.button(
        "🎥 Jelajahi Film",
        width="stretch"
    ):
        st.switch_page("pages/recommendation.py")

with c3:

    if st.button(
        "ℹ️ Tentang",
        width="stretch"
    ):
        st.switch_page("pages/about.py")

# statistics

st.header(
    "📊 Statistik",
    divider="green"
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Film",
    len(movies)
)

c2.metric(
    "Genre",
    movies["genre"].nunique()
)

c3.metric(
    "Rating Tertinggi",
    movies["rating"].max()
)

# genre populer

st.header(
    "🔥 Trending Movies",
    divider="rainbow"
)

trending = (
    movies
    .sort_values(
        "rating",
        ascending=False
    )
    .head(4)
)

cols = st.columns(4)

for col, (_, movie) in zip(
    cols,
    trending.iterrows()
):

    with col:

        st.image(
            movie["poster"],
            width="stretch"
        )

        st.caption(
            movie["title"]
        )

        st.write(
            f"⭐ {movie['rating']}"
        )

st.header(
    "⭐ Top Rated Movies",
    divider="blue"
)


top_movies = (
    movies
    .sort_values(
        "rating",
        ascending=False
    )
    .head(8)
)

for i in range(0, len(top_movies), 4):

    cols = st.columns(4)

    batch = top_movies.iloc[i:i+4]

    for col, (_, movie) in zip(
        cols,
        batch.iterrows()
    ):

        with col:

            st.image(
                movie["poster"],
                width="stretch"
            )

            st.write(
                movie["title"]
            )


st.header(
    "🎭 Browse by Genre",
    divider="orange"
)

genres = (
    movies["genre"]
    .unique()
)

genre_cols = st.columns(
    len(genres)
)

for col, genre in zip(
    genre_cols,
    genres
):

    with col:

        st.button(
            genre,
            width="stretch"
        )

# fitur

st.markdown("## ✨ Fitur Utama")

f1, f2 = st.columns(2)

with f1:

    st.success("🤖 Chatbot Interaktif")
    st.success("🎬 Rekomendasi Film")
    st.success("📖 Detail Film")

with f2:

    st.success("⚙️ Finite State Machine")
    st.success("🔍 Regex Intent Recognition")
    st.success("💬 Context Memory")

# footer

st.markdown("---")

st.caption(
    "MovieBot © 2026 | Teori Bahasa dan Otomata"
)
