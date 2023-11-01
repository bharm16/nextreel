import queue
import threading
from queue import Queue
import time
from flask_login import current_user

from nextreel.db_config import db_config
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
    def __init__(self, db_config, queue, criteria=None):
        self.db_config = db_config
        self.queue = queue
        self.movie_fetcher = ImdbRandomMovieFetcher(self.db_config)
        self.criteria = criteria or {}  # Use the provided criteria or an empty dict

        self.stop_thread = False  # Initialize the stop flag
        self.lock = threading.Lock()

        # Initialize the populate thread here
        self.populate_thread = threading.Thread(target=self.populate)
        self.populate_thread.daemon = True  # Set the thread as a daemon
        self.populate_thread.start()

    def set_criteria(self, new_criteria):
        self.criteria = new_criteria

    def stop_populate_thread(self):
        with self.lock:
            print("Stopping the populate thread...")
            self.stop_thread = True
        self.populate_thread.join()  # Wait for the thread to complete

    def empty_queue(self):
        """Empty the movie queue."""
        with self.lock:  # Ensure thread safety
            while not self.queue.empty():
                try:
                    self.queue.get_nowait()
                except queue.Empty:
                    break
            print("Emptied the movie queue.")

    def populate(self):
        # Initialize sets for watched_movies and watchlist_movies
        watched_movies = set()
        watchlist_movies = set()

        # Loop infinitely, but check the stop_thread flag at each iteration
        while not self.stop_thread:
            print("Running the populate_movie_queue loop...")

            # If the user is authenticated, update watched and watchlist movies
            if current_user and current_user.is_authenticated:
                watched_movies, watchlist_movies = _get_user_data()

            # Check if the queue size is less than 2 and populate accordingly
            if self.queue.qsize() < 2:
                print("Fetching 25 movies from IMDb...")
                self.load_movies_into_queue(watched_movies, watchlist_movies)

            # Sleep for 1 second before the next iteration
            time.sleep(1)

        # This print statement will execute when the thread is stopping.
        print("Stopping the populate thread...")

    def is_thread_alive(self):
        return self.populate_thread.is_alive()

    def load_movies_into_queue(self, watched_movies, watchlist_movies):
        # Fetch a batch of 25 movies based on the criteria
        rows = self.movie_fetcher.fetch_random_movies25(self.criteria)
        print(f"Fetched {len(rows)} movies.")

        # If there are rows to process
        if rows:
            # Iterate through each row
            for row in rows:
                # Acquire the lock and check the stop_thread flag
                with self.lock:
                    if self.stop_thread:
                        print("Stopping populate_movie_queue because stop_thread is True.")
                        return  # Stop the current operation

                # Get the tconst value from the row
                tconst = row['tconst'] if row else None
                print(f"Processing movie with tconst: {tconst}")

                # Check if the movie is not in watched or watchlist sets
                if tconst and (tconst not in watched_movies) and (tconst not in watchlist_movies):
                    print("Movie passes the watched and watchlist check.")

                    # Wait until the queue size drops below 10
                    while self.queue.qsize() >= 10:
                        print("Queue size is 10 or more, waiting...")
                        time.sleep(1)  # Wait for 1 second before re-checking

                    # Create a Movie object and fetch its IMDb data
                    movie = Movie(tconst, self.db_config)
                    movie_data_imdb = movie.get_movie_data()

                    # Fetch additional movie data from TMDb
                    tmdb_id = get_tmdb_id_by_tconst(tconst)
                    movie_data_tmdb = get_movie_info_by_tmdb_id(tmdb_id)

                    # Combine the IMDb and TMDb data
                    movie_data = {
                        'IMDb': movie_data_imdb,
                        'TMDb': movie_data_tmdb
                    }

                    # Add the movie data to the queue
                    self.queue.put(movie_data_imdb)
                    print("Added movie to movie queue.")

                    # Update the database if title basics are empty
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


def main():
    # Assuming db_config is a dictionary containing your DB settings

    movie_queue = Queue()

    # Initialize the MovieQueue object
    movie_queue_manager = MovieQueue(db_config, movie_queue)

    # Setting your specific criteria
    criteria = {
        "min_year": 1900,
        "max_year": 2023,
        "min_rating": 7.0,
        "max_rating": 10,
        "title_type": "movie",
        "language": "en",
        "genres": ["Action", "Drama"]
    }
    movie_queue_manager.set_criteria(criteria)

    # Wait for a few seconds to let the populate method do its work
    time.sleep(5)

    # Stop the populate thread
    movie_queue_manager.stop_populate_thread()

    movie_queue_manager.empty_queue()


    # Check if the thread is still alive
    print(f"Is thread still alive? {movie_queue_manager.is_thread_alive()}")


# This ensures the main function is only run when this script is executed, and not if it's imported as a module
if __name__ == "__main__":
    main()
