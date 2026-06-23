import pandas as pd

class MovieEngine:

    def __init__(self):

        self.movies = pd.read_csv(
            "data/movies.csv"
        )

        self.movies.fillna(
            "",
            inplace=True
        )

    # get all movies

    def get_all_movies(self):

        return (
            self.movies
            .to_dict("records")
        )

    # movies by genre

    def get_movies_by_genre(
        self,
        genre,
        limit=10
    ):

        result = self.movies[

            self.movies["genre"]
            .astype(str)
            .str.lower()
            .str.contains(
                genre.lower(),
                na=False
            )
        ]

        return (
            result
            .head(limit)
            .to_dict("records")
        )

    # get movie by title

    def get_movie_by_title(
        self,
        title
    ):

        result = self.movies[

            self.movies["title"]
            .astype(str)
            .str.lower()
            ==
            title.lower()
        ]

        if len(result) == 0:

            return None

        return (
            result
            .iloc[0]
            .to_dict()
        )

    # find best match movie by keyword

    def find_best_match(
        self,
        keyword
    ):

        result = self.movies[

            self.movies["title"]
            .astype(str)
            .str.lower()
            .str.contains(
                keyword.lower(),
                na=False
            )
        ]

        if len(result) == 0:

            return None

        return (
            result
            .iloc[0]
            .to_dict()
        )

    # search movies by keyword

    def search_movie(
        self,
        keyword,
        limit=10
    ):

        result = self.movies[

            self.movies["title"]
            .astype(str)
            .str.lower()
            .str.contains(
                keyword.lower(),
                na=False
            )
        ]

        return (
            result
            .head(limit)
            .to_dict("records")
        )

    # similar movies by genre

    def get_similar_movies(
        self,
        genre,
        current_title,
        limit=5
    ):

        result = self.movies[

            (
                self.movies["genre"]
                .astype(str)
                .str.lower()
                .str.contains(
                    genre.lower(),
                    na=False
                )
            )
            &
            (
                self.movies["title"]
                .str.lower()
                !=
                current_title.lower()
            )
        ]

        return (
            result
            .head(limit)
            .to_dict("records")
        )

    # top rated movies

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

        return (
            result
            .to_dict("records")
        )

    # random movie

    def get_random_movie(self):

        if len(self.movies) == 0:

            return None

        return (

            self.movies

            .sample(1)

            .iloc[0]

            .to_dict()
        )

    # statistics

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

                float(

                    self.movies[
                        "rating"
                    ].max()
                ),

            "average_rating":

                round(

                    float(

                        self.movies[
                            "rating"
                        ].mean()

                    ),

                    2
                )
        }
