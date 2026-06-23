import random

from chatbot.intent import IntentRecognizer
from chatbot.movie_engine import MovieEngine


class MovieFSM:

    def __init__(self):

        self.intent = IntentRecognizer()

        self.engine = MovieEngine()

        self.state = "MAIN_MENU"

        self.last_movies = []

        self.current_movie = None

        self.current_genre = None

    # response builders

    def text_response(
        self,
        message
    ):

        return {
            "type": "text",
            "message": message
        }

    def movie_response(
        self,
        message,
        movies
    ):

        return {
            "type": "movie",
            "message": message,
            "movies": movies
        }

    # process

    def process(
        self,
        user_text
    ):

        intent, value = (
            self.intent.recognize(
                user_text
            )
        )

        # greating

        if intent == "greeting":

            greetings = [

                "Halo 👋 Saya MovieBot. Lagi ingin nonton film apa hari ini?",

                "Hai 🎬 Saya siap membantu mencarikan film yang cocok untukmu.",

                "Hello 🍿 Mau cari rekomendasi film?"
            ]

            return self.text_response(
                random.choice(
                    greetings
                )
            )

        # thanks

        elif intent == "thanks":

            return self.text_response(
                "Sama-sama 😊 Semoga menemukan film yang seru untuk ditonton."
            )

        # top movues

        elif intent == "top_movies":

            movies = (
                self.engine
                .get_top_rated_movies()
            )

            self.last_movies = movies

            return self.movie_response(
                "🏆 Film dengan rating tertinggi:",
                movies
            )

        # random movie

        elif intent == "random_movie":

            movies = (
                self.engine
                .get_all_movies()
            )

            movie = (
                random.choice(
                    movies
                )
            )

            self.current_movie = movie

            return self.movie_response(
                "🎲 Coba film ini:",
                [movie]
            )

        # recommendation

        elif intent == "recommendation":

            movies = (
                self.engine
                .get_movies_by_genre(
                    value
                )
            )

            if len(movies) == 0:

                return self.text_response(
                    f"Maaf, saya belum menemukan film genre {value}"
                )

            self.current_genre = value

            self.last_movies = movies

            return self.movie_response(
                f"🎬 Berikut rekomendasi film genre {value}:",
                movies
            )


        # movie number

        elif intent == "movie_number":

            if not self.last_movies:

                return self.text_response(
                    "Belum ada daftar film yang dipilih."
                )

            index = value - 1

            if (
                index < 0
                or index >= len(
                    self.last_movies
                )
            ):

                return self.text_response(
                    "Nomor film tidak tersedia."
                )

            movie = (
                self.last_movies[
                    index
                ]
            )

            self.current_movie = movie

            return self.movie_response(
                "🎥 Detail film:",
                [movie]
            )

        # detail

        elif intent == "detail":

            movie = (
                self.engine
                .find_best_match(
                    value
                )
            )

            if movie is None:

                return self.text_response(
                    "Film tidak ditemukan."
                )

            self.current_movie = movie

            return self.movie_response(
                "🎥 Saya menemukan film ini:",
                [movie]
            )

        # rating

        elif intent == "rating_question":

            if not self.current_movie:

                return self.text_response(
                    "Pilih film terlebih dahulu."
                )

            return self.text_response(
                f"⭐ Rating {self.current_movie['title']} adalah {self.current_movie['rating']}/10"
            )


        # genre

        elif intent == "genre_question":

            if not self.current_movie:

                return self.text_response(
                    "Pilih film terlebih dahulu."
                )

            return self.text_response(
                f"🎭 Genre film ini adalah {self.current_movie.get('genre','Tidak diketahui')}"
            )

        # year

        elif intent == "year_question":

            if not self.current_movie:

                return self.text_response(
                    "Pilih film terlebih dahulu."
                )

            return self.text_response(
                f"📅 Film ini dirilis pada tahun {self.current_movie.get('year','Tidak diketahui')}"
            )

        # similar movies

        elif intent == "similar_movie":

            if not self.current_movie:

                return self.text_response(
                    "Pilih film terlebih dahulu."
                )

            genre = (
                self.current_movie[
                    "genre"
                ]
            )

            movies = (
                self.engine
                .get_movies_by_genre(
                    genre
                )
            )

            self.last_movies = movies

            return self.movie_response(
                "🎬 Kalau kamu suka film itu, mungkin kamu juga suka:",
                movies
            )

        # back

        elif intent == "back":

            self.state = "MAIN_MENU"

            return self.text_response(
                "🏠 Kembali ke menu utama. Kamu bisa meminta rekomendasi film atau mencari judul film."
            )

        # unknown

        return self.text_response(
            """
            Maaf, saya belum memahami maksudmu 😅

            Coba salah satu contoh berikut:

            • rekomendasi film horror
            • film terbaik
            • film populer
            • cari film interstellar
            • film 1
            • yang mirip
            • surprise me
         """
        )
