import imdb

from nextreel.scripts.db_config_scripts import db_config
from nextreel.scripts.mysql_query_builder import get_db_connection
from nextreel.scripts.set_filters_for_nextreel_backend import ImdbRandomMovieFetcher

get_db_connection(db_config)


class Movie:
    def __init__(self, tconst, db_config):
        self.tconst = tconst
        self.db_config = db_config
        self.movie_data = {}

    def fetch_info_from_imdb(self):
        """Fetch movie information from IMDb using IMDbPY."""
        imdbId = int(self.tconst[2:])
        ia = imdb.IMDb()
        return ia.get_movie(imdbId)

    def store_movie_data(self, movie):
        self.movie_data = {
            "title": movie.get('title', 'N/A'),
            "imdb_id": movie.getID(),
            "genres": ', '.join(movie.get('genres', ['N/A'])),
            "directors": ', '.join([director['name'] for director in movie.get('director', [])]),
            "writers": next((writer['name'] for writer in movie.get('writer', []) if 'name' in writer), "N/A"),
            "cast": ', '.join([actor['name'] for actor in movie.get('cast', [])][:3]),
            "runtimes": ', '.join(movie.get('runtimes', ['N/A'])),
            "countries": ', '.join(movie.get('countries', ['N/A'])),
            "languages": movie.get('languages', ['N/A'])[0] if movie.get('languages') else 'N/A',
            # "languages": ', '.join(movie.get('languages', ['N/A'])) if movie.get('languages') else 'N/A',
            "rating": movie.get('rating', 'N/A'),
            "votes": movie.get('votes', 'N/A'),
            "plot": movie.get('plot', ['N/A'])[0],
            "poster_url": movie.get_fullsizeURL(),
            "year": movie.get('year')
        }

    def get_movie_data(self):
        movie_data = self.fetch_info_from_imdb()
        self.store_movie_data(movie_data)
        return self.movie_data


# Main function to run the program
def main(criteria):
    movie_fetcher = ImdbRandomMovieFetcher(db_config)
    row = movie_fetcher.fetch_random_movie(criteria)

    if not row:
        print("No movies found based on the given criteria.")
        return None

    movie = Movie(row['tconst'], db_config)
    movie_data = movie.get_movie_data()

    print("Fetched movie genres:", movie_data.get('genres'))


# # Example usage
if __name__ == "__main__":
    criteria = {
        "min_year": 1900,
        "max_year": 2023,
        "min_rating": 7.0,
        "max_rating": 10,
        "title_type": "movie",
        "language": "en",
        "genres": ["Action", "Drama"]
    }

    main(criteria)
