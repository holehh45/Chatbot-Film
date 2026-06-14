from enum import Enum, auto
import random
from chatbot.intent import IntentRecognizer
from chatbot.movie_engine import MovieEngine

class State(Enum):
    START = auto()
    MAIN_MENU = auto()
    RECOMMENDATION = auto()
    DETAIL = auto()

class MovieFSM:
    def __init__(self):
        self.state = State.START
        self.movie_engine = MovieEngine()
        self.intent_recognizer = IntentRecognizer()
        # Menyimpan hasil rekomendasi terakhir
        self.last_movies = []

        # Film yang sedang dibahas
        self.current_movie = None

    # ==========================
    # RESPONSE HELPERS
    # ==========================

    def text_response(self, message):
        return {
            "type": "text",
            "data": message
        }

    def movie_response(self, movie):
        return {
            "type": "movie",
            "data": movie
        }
    def natural_movie_comment(self, movie):

        rating = float(movie["rating"])

        if rating >= 8.5:
            return (
                "🔥 Film ini sangat direkomendasikan dan menjadi salah satu favorit penonton."
            )

        elif rating >= 7:
            return (
                "🍿 Film ini cukup populer dan layak masuk daftar tontonan Anda."
            )

        return (
            "🎥 Film ini bisa menjadi pilihan menarik untuk dicoba."
    )

    # ==========================
    # MAIN PROCESS
    # ==========================

    def process(self, text):
        intent, entity = (
            self.intent_recognizer.recognize(text)
        )

        # ==========================
        # START
        # ==========================

        if self.state == State.START:
            if intent == "greeting":
                self.state = State.MAIN_MENU
            greetings = [

    "👋 Halo! Saya MovieBot. Film apa yang ingin Anda cari hari ini?",

    "🎬 Hai! Saya siap membantu menemukan film yang cocok untuk Anda.",

    "🍿 Halo! Sebutkan genre favorit Anda, dan saya akan memberikan rekomendasi."
]

            return self.text_response(
                random.choice(greetings)
            )
        
        # ==================================
        # FOLLOW UP CONVERSATION
        # ==================================

        if intent == "thanks":

            return self.text_response(
                random.choice([
                    "Sama-sama 😊",
                    "Dengan senang hati 🍿",
                    "Semoga rekomendasinya membantu 🎬"
                ])
            )

        if intent == "rating_question":

            if self.current_movie:

                return self.text_response(
                    f"⭐ Film **{self.current_movie['title']}** memiliki rating **{self.current_movie['rating']}**."
                )

            return self.text_response(
                "Film apa yang ingin Anda tanyakan?"
            )

        if intent == "genre_question":

            if self.current_movie:

                return self.text_response(
                    f"🎭 Film **{self.current_movie['title']}** termasuk genre **{self.current_movie['genre']}**."
                )

            return self.text_response(
                "Silakan pilih film terlebih dahulu."
            )

        if intent == "year_question":

            if self.current_movie:

                return self.text_response(
                    f"📅 Film **{self.current_movie['title']}** dirilis pada tahun **{self.current_movie['year']}**."
                )

            return self.text_response(
                "Silakan pilih film terlebih dahulu."
            )

        if intent == "similar_movie":

            if self.current_movie:

                similar_movies = (
                    self.movie_engine.get_similar_movies(
                        self.current_movie["genre"],
                        self.current_movie["title"]
                    )
                )

                result = (
                    f"🎬 Jika Anda menyukai **{self.current_movie['title']}**, saya juga merekomendasikan:\n\n"
                )

                for idx, (_, row) in enumerate(
                    similar_movies.iterrows(),
                    start=1
                ):

                    result += (
                        f"{idx}. {row['title']} ⭐ {row['rating']}\n"
                    )

                return self.text_response(
                    result
                )

            return self.text_response(
                "Silakan pilih film terlebih dahulu."
            )
        # ==========================
        # MAIN MENU
        # ==========================

        if self.state == State.MAIN_MENU:
            # ----------------------
            # RECOMMENDATION
            # ----------------------

            if intent == "recommendation":
                if not entity:
                    return self.text_response(
                        "Sebutkan genre, misalnya:\n\nrekomendasi film action"
                    )

                movies = (
                    self.movie_engine
                    .get_movies_by_genre(entity)
                )

                if len(movies) == 0:
                    return self.text_response(
                        "Genre tidak ditemukan."
                    )

                self.last_movies = []
                result = (
                     f"🎬 Saya menemukan beberapa film genre **{entity.title()}** yang mungkin Anda sukai:\n\n"
                )

                for index, (_, row) in enumerate(
                    movies.iterrows(),
                    start=1
                ):
                    self.last_movies.append(
                        row["title"]
                    )
                    result += (
                        f"{index}. "
                        f"{row['title']} "
                        f"(⭐ {row['rating']})\n"
                    )

                result += """
### Pilih Film

* film 1
* film 2
* film 3

atau

* detail nama_film
"""
                self.state = (
                    State.RECOMMENDATION
                )
                return self.text_response(
                    result
                )

            # ----------------------
            # DETAIL FILM
            # ----------------------

            if (
                intent == "detail"
                and isinstance(entity, str)
            ):
                movie = (
                    self.movie_engine
                    .get_movie(entity)
                )

                if movie is None:
                    return self.text_response(
                        "Film tidak ditemukan."
                    )

                self.state = State.DETAIL
                movie["comment"] = (
                    self.natural_movie_comment(movie)(
                        movie
                    )
                )
                self.current_movie = movie

                return self.movie_response(
                    movie
                )

            return self.text_response("""Saya bisa membantu:

* rekomendasi film action
* rekomendasi film sci-fi
* detail interstellar
""")

        # ==========================
        # RECOMMENDATION STATE
        # ==========================

        if self.state == State.RECOMMENDATION:
            # film 1
            # film 2

            if intent == "movie_number":
                if not self.last_movies:
                    return self.text_response(
                        "Belum ada rekomendasi film."
                    )

                idx = entity - 1

                if (
                    idx < 0
                    or idx >= len(self.last_movies)
                ):
                    return self.text_response(
                        "Nomor film tidak valid."
                    )

                movie = (
                    self.movie_engine
                    .get_movie(
                        self.last_movies[idx]
                    )
                )

                if movie is None:
                    return self.text_response(
                        "Film tidak ditemukan."
                    )

                self.state = State.DETAIL
                movie["comment"] = (
                    self.natural_movie_comment(movie)
                )
                self.current_movie = movie
                return self.movie_response(
                    movie
                )

            # detail interstellar

            if (
                intent == "detail"
                and isinstance(entity, str)
            ):
                movie = (
                    self.movie_engine
                    .get_movie(entity)
                )

                if movie is None:
                    return self.text_response(
                        "Film tidak ditemukan."
                    )

                self.state = State.DETAIL
                movie["comment"] = (
                    self.natural_movie_comment(movie)
                )
                self.current_movie = movie
                return self.movie_response(
                    movie
                )

            return self.text_response("""Silakan pilih film:

* film 1
* film 2
* film 3

atau

* detail nama_film
""")

        # ==========================
        # DETAIL STATE
        # ==========================

        if self.state == State.DETAIL:
            if intent == "recommendation":
                self.state = State.MAIN_MENU
                return self.process(text)

            if (
                intent == "detail"
                and isinstance(entity, str)
            ):
                movie = (
                    self.movie_engine
                    .get_movie(entity)
                )

                if movie:
                    movie["comment"] = (
                        self.natural_movie_comment(movie)
                    )
                    self.current_movie = movie
                    return self.movie_response(
                        movie
                    )

            return self.text_response("""💬 Perintah yang tersedia

* rekomendasi film action
* rekomendasi film drama
* detail inception
""")

        return self.text_response(
            "Maaf, saya tidak memahami perintah tersebut."
        )