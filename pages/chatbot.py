import random
import streamlit as st

from chatbot.fsm import MovieFSM

st.set_page_config(
    page_title="MovieBot Chat",
    page_icon="🎬",
    layout="wide",
)

# ==========================
# HELPER RENDER
# ==========================

def render_message(content):
    if content["type"] == "text":
        st.markdown(content["data"])

    elif content["type"] == "movie":
        movie = content["data"]
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                if "poster" in movie and movie["poster"]:
                    st.image(
                    movie["poster"],
                    width="stretch"
                )
            with col2:
                st.subheader(movie["title"])
                st.write(f"🎭 Genre: {movie.get('genre','-')}")
                st.write(f"📅 Tahun: {movie.get('year','-')}")
                st.write(f"⭐ Rating: {movie.get('rating','-')}")

                if "overview" in movie and movie["overview"]:
                    st.markdown("### 📖 Sinopsis")
                    st.write(movie["overview"])

                st.divider()

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("🎬 Film Serupa", key=f"similar_{movie['title']}", use_container_width=True):
                        response = st.session_state.fsm.process("film serupa")
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()

                with col_b:
                    if st.button("⭐ Rating", key=f"rating_{movie['title']}", use_container_width=True):
                        response = st.session_state.fsm.process("ratingnya berapa")
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()

                col_c, col_d = st.columns(2)
                with col_c:
                    if st.button("🎭 Genre", key=f"genre_{movie['title']}", use_container_width=True):
                        response = st.session_state.fsm.process("genrenya apa")
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()

                with col_d:
                    if st.button("📅 Tahun", key=f"year_{movie['title']}", use_container_width=True):
                        response = st.session_state.fsm.process("tahun berapa")
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()


# ==========================
# HEADER
# ==========================

st.header("🤖 MovieBot", divider="rainbow")

top1, top2 = st.columns([8, 1])
with top2:
    if st.button("🏠", use_container_width=True):
        st.switch_page("app.py")


# ==========================
# SESSION STATE
# ==========================

if "fsm" not in st.session_state:
    st.session_state.fsm = MovieFSM()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": {
                "type": "text",
                "data": """# 🍿 Selamat Datang di MovieBot

Saya dapat membantu Anda menemukan film yang menarik.

### Contoh

🎬 rekomendasi film action

🎬 rekomendasi film sci-fi

📖 detail interstellar

### Anda juga bisa bertanya

⭐ ratingnya berapa?

🎭 genrenya apa?

📅 tahun berapa?

🎬 film serupa
""",
            },
        }
    ]


# ==========================
# CHAT HISTORY
# ==========================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        render_message(message["content"])


# ==========================
# INPUT
# ==========================

prompt = st.chat_input("Tanyakan film favoritmu...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": {"type": "text", "data": prompt},
    })

    loading_text = random.choice([
        "🎬 Mencari film terbaik...",
        "🍿 Menyiapkan rekomendasi...",
        "🔍 Menelusuri database film...",
        "⭐ Memilih film yang cocok...",
    ])

    with st.spinner(loading_text):
        response = st.session_state.fsm.process(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
