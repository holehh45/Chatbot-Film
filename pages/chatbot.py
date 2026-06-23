import random
import streamlit as st

from chatbot.fsm import MovieFSM

# page configuration

st.set_page_config(
    page_title="MovieBot Chat",
    page_icon="🎬",
    layout="wide",
)

# function to render chatbot response

def render_message(
    content,
    msg_index
):

    # text response

    if content["type"] == "text":

        st.markdown(
            content["message"]
        )

    # movie response

    elif content["type"] == "movie":

        st.markdown(
            content["message"]
        )

        movies = content["movies"]

        for idx, movie in enumerate(
            movies,
            start=1
        ):

            with st.container():

                st.divider()

                col1, col2 = st.columns(
                    [1, 2]
                )

                # poster

                with col1:

                    poster = (
                        movie.get(
                            "poster_url"
                        )
                        or
                        movie.get(
                            "poster"
                        )
                    )

                    if poster:

                        st.image(
                            poster,
                            use_container_width="stretch"
                        )

                # details

                with col2:

                    st.subheader(
                        f"{idx}. {movie.get('title','-')}"
                    )

                    if movie.get(
                        "genre"
                    ):

                        st.write(
                            f"🎭 Genre: {movie['genre']}"
                        )

                    if movie.get(
                        "year"
                    ):

                        st.write(
                            f"📅 Tahun: {movie['year']}"
                        )

                    if movie.get(
                        "rating"
                    ):

                        st.write(
                            f"⭐ Rating: {movie['rating']}"
                        )

                    if movie.get(
                        "overview"
                    ):

                        with st.expander(
                            "📖 Sinopsis"
                        ):

                            st.write(
                                movie[
                                    "overview"
                                ]
                            )

                    st.divider()

                    # action buttons

                    btn1, btn2 = st.columns(
                        2
                    )

                    with btn1:

                        if st.button(
                            "🎬 Detail",
                            key=f"detail_{msg_index}_{idx}_{movie['title']}"
                        ):

                            response = (
                                st.session_state
                                .fsm
                                .process(
                                    f"detail {movie['title']}"
                                )
                            )

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": response
                                }
                            )

                            st.rerun()

                    with btn2:

                        if st.button(
                            "🎯 Pilih Film",
                            key=f"select_{msg_index}_{idx}_{movie['title']}"
                        ):

                            response = (
                                st.session_state
                                .fsm
                                .process(
                                    f"film {idx}"
                                )
                            )

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": response
                                }
                            )

                            st.rerun()

                    btn3, btn4 = st.columns(
                        2
                    )

                    with btn3:

                        if st.button(
                            "⭐ Rating",
                            key=f"rating_{msg_index}_{idx}_{movie['title']}"
                        ):

                            response = (
                                st.session_state
                                .fsm
                                .process(
                                    "ratingnya berapa"
                                )
                            )

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": response
                                }
                            )

                            st.rerun()

                    with btn4:

                        if st.button(
                            "🎭 Genre",
                            key=f"genre_{msg_index}_{idx}_{movie['title']}"
                        ):

                            response = (
                                st.session_state
                                .fsm
                                .process(
                                    "genrenya apa"
                                )
                            )

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": response
                                }
                            )

                            st.rerun()

                    btn5, btn6 = st.columns(
                        2
                    )

                    with btn5:

                        if st.button(
                            "📅 Tahun",
                            key=f"year_{msg_index}_{idx}_{movie['title']}"
                        ):

                            response = (
                                st.session_state
                                .fsm
                                .process(
                                    "tahun berapa"
                                )
                            )

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": response
                                }
                            )

                            st.rerun()

                    with btn6:

                        if st.button(
                            "🎥 Film Serupa",
                            key=f"similar_{msg_index}_{idx}_{movie['title']}"
                        ):

                            response = (
                                st.session_state
                                .fsm
                                .process(
                                    "film serupa"
                                )
                            )

                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": response
                                }
                            )

                            st.rerun()



# header

st.header(
    "🎬 MovieBot",
    divider="rainbow"
)

top1, top2 = st.columns(
    [8, 1]
)

with top2:

    if st.button(
        "🏠",
        use_container_width="stretch"
    ):

        st.switch_page(
            "app.py"
        )

# initialize FSM and messages

if "fsm" not in st.session_state:

    st.session_state.fsm = (
        MovieFSM()
    )

if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "assistant",

            "content": {

                "type": "text",

                "message": """
            # 🍿 Selamat Datang di MovieBot

            Saya dapat membantu menemukan film yang menarik.

            ### Contoh

            🎬 rekomendasi film horror

            🎬 rekomendasi film action

            🎬 rekomendasi film drama

            🎲 surprise me

            🏆 film terbaik

            📖 detail interstellar

            ### Follow Up

            ⭐ ratingnya berapa

            🎭 genrenya apa

            📅 tahun berapa

            🎥 film serupa
            """
            }
        }
    ]


# chat history


for msg_index, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        render_message(
            message["content"],
            msg_index
        )

# chat input

prompt = st.chat_input(
    "Tanyakan film favoritmu..."
)

if prompt:

    st.session_state.messages.append(

        {
            "role": "user",

            "content": {

                "type": "text",

                "message": prompt
            }
        }
    )

    loading_text = random.choice([

        "🎬 Mencari film terbaik...",

        "🍿 Menyiapkan rekomendasi...",

        "🔍 Menelusuri database film...",

        "⭐ Memilih film yang cocok..."
    ])

    with st.spinner(
        loading_text
    ):

        response = (
            st.session_state
            .fsm
            .process(
                prompt
            )
        )

    st.session_state.messages.append(

        {
            "role": "assistant",

            "content": response
        }
    )

    st.rerun()
