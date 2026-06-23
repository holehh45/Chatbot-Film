import re


class IntentRecognizer:

    GENRE_MAP = {

        "aksi": "action",
        "action": "action",

        "komedi": "comedy",
        "comedy": "comedy",
        "lucu": "comedy",

        "drama": "drama",

        "horor": "horror",
        "horror": "horror",

        "romantis": "romance",
        "romance": "romance",

        "animasi": "animation",
        "animation": "animation",
        "kartun": "animation",

        "sci-fi": "sci-fi",
        "scifi": "sci-fi",
        "fiksi ilmiah": "sci-fi"
    }

    ORDINAL_MAP = {

        "pertama": 1,
        "kedua": 2,
        "ketiga": 3,
        "keempat": 4,
        "kelima": 5,
        "keenam": 6,
        "ketujuh": 7,
        "kedelapan": 8,
        "kesembilan": 9,
        "kesepuluh": 10
    }

    def recognize(self, text):

        text = text.lower().strip()

        # greeting

        if re.search(
            r"\b(halo|hai|hello|hi|pagi|siang|sore|malam)\b",
            text
        ):

            return (
                "greeting",
                None
            )

        # thanks

        if re.search(
            r"(terima kasih|makasih|thanks|thank you)",
            text
        ):

            return (
                "thanks",
                None
            )

        # kembali

        if re.search(
            r"(menu|kembali|home|awal)",
            text
        ):

            return (
                "back",
                None
            )

        # folw up

        if re.search(
            r"(ratingnya|berapa rating)",
            text
        ):

            return (
                "rating_question",
                None
            )

        if re.search(
            r"(genre apa|genrenya)",
            text
        ):

            return (
                "genre_question",
                None
            )

        if re.search(
            r"(tahun berapa|kapan rilis|rilis kapan)",
            text
        ):

            return (
                "year_question",
                None
            )

        if re.search(
            r"(film serupa|film mirip|mirip dengan itu|yang mirip|sejenis|rekomendasi serupa)",
            text
        ):

            return (
                "similar_movie",
                None
            )

        # top movie

        if re.search(
            r"(film terbaik|rating tertinggi|film populer|film terkenal|top movie|top film)",
            text
        ):

            return (
                "top_movies",
                None
            )

        # film random

        if re.search(
            r"(bebas|acak|surprise me|apa saja|terserah)",
            text
        ):

            return (
                "random_movie",
                None
            )

        # nomer film
        
        number_match = re.search(
            r"(film|nomor)\s*(\d+)",
            text
        )

        if number_match:

            return (
                "movie_number",
                int(number_match.group(2))
            )

        for word, number in self.ORDINAL_MAP.items():

            if f"yang {word}" in text:

                return (
                    "movie_number",
                    number
                )

        # detail

        detail_match = re.search(
            r"(detail|info|informasi)\s+(.+)",
            text
        )

        if detail_match:

            return (
                "detail",
                detail_match.group(2).strip()
            )
        
        # search film

        search_match = re.search(
            r"(cari film|search film)\s+(.+)",
            text
        )

        if search_match:

            return (
                "detail",
                search_match.group(2).strip()
            )

        # rekomendasi

        for keyword, genre in self.GENRE_MAP.items():

            if keyword in text:

                if re.search(
                    r"(rekomendasi|sarankan|film bagus|ingin film|suka genre|film genre|film|nonton|tontonan|film seru|ada film)",
                    text
                ):

                    return (
                        "recommendation",
                        genre
                    )

        # Judul pendek

        words = text.split()

        if (
            len(words) <= 5
            and not re.search(r"\d+", text)
        ):

            return (
                "detail",
                text
            )

        return (
            "unknown",
            None
        )
