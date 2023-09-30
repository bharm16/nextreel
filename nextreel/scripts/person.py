# person.py
from concurrent.futures import ThreadPoolExecutor

import imdb

from nextreel.scripts.movie import Movie
from nextreel.scripts.mysql_query_builder import execute_query, \
    GET_NCONST_FROM_ACTOR_NAME_QUERY, GET_ALL_MOVIES_BY_ACTOR_QUERY  # Import your query execution function


class Person:
    def __init__(self, db_config, actor_name):
        self.db_config = db_config
        self.actor_name = actor_name
        self.actor_nconst = self.get_nconst()
        self.actor_info = None if self.actor_nconst is None else self.fetch_info_from_imdb()

    def get_nconst(self):
        """Fetch the nconst (IMDb identifier) for an actor based on their name."""
        # Use the SQL query from sql_queries.py
        query = GET_NCONST_FROM_ACTOR_NAME_QUERY

        # Query parameters
        parameters = [self.actor_name]

        # Execute the query
        result = execute_query(self.db_config, query, parameters, fetch='one')

        return result['nconst'] if result else None

    def fetch_info_from_imdb(self):
        """Fetch actor information from IMDb."""
        # Initialize IMDb object
        ia = imdb.IMDb()

        # Fetch actor information from IMDb
        actor_info = ia.get_person(self.actor_nconst[2:])  # Remove the 'nm' prefix

        return actor_info

    def get_all_movies_by_actor(db_config, nconst):
        # Use the query from sql_queries.py
        query = GET_ALL_MOVIES_BY_ACTOR_QUERY

        parameters = [nconst]
        print("Generated SQL Query for get_all_movies_by_actor:", query)
        print("Query Parameters:", parameters)

        all_movies = execute_query(db_config, query, parameters, fetch='all')
        movies_data = []

        def fetch_and_append_movie_data(movie):
            # Create a Movie object
            movie_obj = Movie(movie['tconst'], db_config)
            # Get movie data and append to movies_data list
            movies_data.append(movie_obj.get_movie_data())

        if all_movies:
            # Increase max_workers to a higher value depending on your system's capability
            with ThreadPoolExecutor(max_workers=20) as executor:
                executor.map(fetch_and_append_movie_data, all_movies)

        return movies_data if movies_data else None
