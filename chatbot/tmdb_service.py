import requests
import streamlit as st


class TMDBService:

    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):

        self.api_key = st.secrets[
            "TMDB_API_KEY"
        ]

    def search_movie(self, title):

        url = (
            f"{self.BASE_URL}/search/movie"
        )

        params = {
            "api_key": self.api_key,
            "query": title
        }

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        if data["results"]:

            return data["results"][0]

        return None