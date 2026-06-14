import pandas as pd

from chatbot.tmdb_service import TMDBService

class MovieEngine:
    def __init__(self):

        self.tmdb = TMDBService()

        self.movies = pd.read_csv(
            "data/movies.csv"
        )

# ==================================
# GET ALL MOVIES
# ==================================

    def get_all_movies(self):

        return self.movies

# ==================================
# GET MOVIES BY GENRE
# ==================================

    def get_movies_by_genre(
        self,
        genre
    ):

        result = self.movies[
            self.movies["genre"]
            .str.lower()
            ==
            genre.lower()
        ]

        return result

# ==================================
# GET MOVIE BY TITLE
# ==================================

    def get_movie(
        self,
        title
    ):

        result = self.movies[
            self.movies["title"]
            .str.lower()
            ==
            title.lower()
        ]

        if len(result) > 0:

            return (
                result
                .iloc[0]
                .to_dict()
            )

        return None

# ==================================
# SEARCH MOVIE
# ==================================

    def search_movie(
        self,
        keyword
    ):

        result = self.movies[
            self.movies["title"]
            .str.lower()
            .str.contains(
                keyword.lower(),
                na=False
            )
        ]

        return result

# ==================================
# SIMILAR MOVIES
# ==================================

    def get_similar_movies(
        self,
        genre,
        current_title
    ):

        result = self.movies[
            (
                self.movies["genre"]
                .str.lower()
                ==
                genre.lower()
            )
            &
            (
                self.movies["title"]
                != current_title
            )
        ]

        return result.head(4)

# ==================================
# TOP RATED MOVIES
# ==================================

    def get_top_rated_movies(
        self,
        limit=5
    ):

        result = (
            self.movies
            .sort_values(
                by="rating",
                ascending=False
            )
            .head(limit)
        )

        return result

# ==================================
# RANDOM MOVIE
# ==================================

    def get_random_movie(self):

        if len(self.movies) == 0:

            return None

        return (
            self.movies
            .sample(1)
            .iloc[0]
            .to_dict()
        )

# ==================================
# TMDB DATA
# ==================================

    def get_movie_with_tmdb(
        self,
        title
    ):

        try:

            movie = (
                self.tmdb.search_movie(
                    title
                )
            )

            if movie is None:

                return None

            poster = None

            if movie.get(
                "poster_path"
            ):

                poster = (
                    "https://image.tmdb.org/t/p/w500"
                    +
                    movie["poster_path"]
                )

            return {

                "title":
                    movie.get(
                        "title",
                        title
                    ),

                "overview":
                    movie.get(
                        "overview",
                        ""
                    ),

                "rating":
                    movie.get(
                        "vote_average",
                        0
                    ),

                "poster":
                    poster
            }

        except Exception as e:

            print(e)

            return None

# ==================================
# MOVIE STATISTICS
# ==================================

    def get_statistics(self):

        return {

            "total_movies":
                len(
                    self.movies
                ),

            "total_genres":
                self.movies[
                    "genre"
                ].nunique(),

            "highest_rating":
                self.movies[
                    "rating"
                ].max()
        }