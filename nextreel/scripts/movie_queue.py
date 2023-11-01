from queue import Queue
import time
from flask_login import current_user

from nextreel.scripts.get_user_account import get_all_watched_movie_details_by_user, get_all_movies_in_watchlist
from nextreel.scripts.log_movie_to_account import update_title_basics_if_empty
from nextreel.scripts.movie import Movie
from nextreel.scripts.set_filters_for_nextreel_backend import ImdbRandomMovieFetcher
from nextreel.scripts.tmdb_data import get_tmdb_id_by_tconst, get_movie_info_by_tmdb_id


# Import the required modules and functions from your project


def _get_user_data():
    watched_movies = set([movie['tconst'] for movie in get_all_watched_movie_details_by_user(current_user.id)])
    watchlist_movies = set([movie['tconst'] for movie in get_all_movies_in_watchlist(current_user.id)])
    return watched_movies, watchlist_movies


class MovieQueue:
    def __init__(self, db_config, queue):
        self.db_config = db_config
        self.queue = queue  # Use the passed-in queue instance
        self.movie_fetcher = ImdbRandomMovieFetcher(self.db_config)
        self.criteria = {}

    def set_criteria(self, new_criteria):
        self.criteria = new_criteria

    def populate(self):
        watched_movies = set()
        watchlist_movies = set()

        while True:
            print("Running the populate_movie_queue loop...")
            if current_user and current_user.is_authenticated:
                watched_movies, watchlist_movies = _get_user_data()

            if self.queue.qsize() < 2:
                print("Fetching 25 movies from IMDb...")
                self._populate_movies_batch(watched_movies, watchlist_movies)

            time.sleep(1)

    def _populate_movies_batch(self, watched_movies, watchlist_movies):
        rows = self.movie_fetcher.fetch_random_movies25(self.criteria)
        print(f"Fetched {len(rows)} movies.")

        if rows:
            for row in rows:
                tconst = row['tconst'] if row else None
                print(f"Processing movie with tconst: {tconst}")

                if tconst and (tconst not in watched_movies) and (tconst not in watchlist_movies):
                    print("Movie passes the watched and watchlist check.")
                    movie = Movie(tconst, self.db_config)
                    movie_data_imdb = movie.get_movie_data()

                    tmdb_id = get_tmdb_id_by_tconst(tconst)
                    movie_data_tmdb = get_movie_info_by_tmdb_id(tmdb_id)
                    print(f"Fetched additional info from TMDb for movie with tmdb_id: {tmdb_id}")

                    movie_data = {
                        'IMDb': movie_data_imdb,
                        'TMDb': movie_data_tmdb
                    }
                    print(f"Combined movie data: {movie_data}")

                    self.queue.put(movie_data_imdb)
                    print("Added movie to movie queue.")

                    update_title_basics_if_empty(
                        tconst,
                        movie_data_imdb['plot'],
                        movie_data_imdb['poster_url'],
                        movie_data_imdb['languages'],
                        self.db_config
                    )
                    print("Updated title basics if they were empty.")
                else:
                    print("Movie does not pass the watched and watchlist check.")
