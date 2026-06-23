import streamlit as st
import pandas as pd

st.set_page_config(
page_title="Movie Library",
page_icon="🎬",
layout="wide"
)

# header

st.header(
"🎬 Movie Library",
divider="rainbow"
)

col1, col2 = st.columns([8, 1])

with col2:
    if st.button(
"🏠 Dashboard",
width="stretch"
):
        st.switch_page("app.py")

# load data

movies = pd.read_csv(
"data/movies.csv"
)

# FILTER

left, right = st.columns([2, 6])

with left:

    genre = st.selectbox(
        "🎭 Genre",
        ["Semua"]
        +
        sorted(
            movies["genre"]
            .unique()
        )
    )


with right:

    search = st.text_input(
        "🔍 Cari Film"
    )

# filtert data

filtered = movies.copy()

if genre != "Semua":

    filtered = filtered[
        filtered["genre"] == genre
    ]

if search:


    filtered = filtered[
        filtered["title"]
        .str.contains(
            search,
            case=False
        )
    ]

# info

st.caption(
f"Menampilkan {len(filtered)} film"
)

st.divider()

# movie grid

cols = st.columns(4)

for idx, (_, movie) in enumerate(
filtered.iterrows()
):

    with cols[idx % 4]:

        with st.container(
        border=True
    ):

            st.image(
                movie["poster"],
                width="stretch"
            )

            st.markdown(
                f"### {movie['title']}"
            )

            st.caption(
                f"🎭 {movie['genre']}"
            )

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "⭐ Rating",
                movie["rating"]
            )

        with c2:
            st.metric(
                "📅 Tahun",
                movie["year"]
            )

        if st.button(
            "🎬 Detail",
            key=f"detail_{idx}",
            width="stretch"
        ):

            st.session_state.selected_movie = (
                movie["title"]
            )

            st.switch_page(
                "pages/chatbot.py"
            )
