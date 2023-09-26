import json
from datetime import datetime
import logging
import imdb
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from nextreel.scripts.db_config_scripts import user_db_config, db_config  # Import both configs
from nextreel.scripts.getMovieFromIMDB import fetch_movie_info_from_imdb
from nextreel.scripts.mysql_query_builder import execute_query

# Initialize logging
logging.basicConfig(level=logging.INFO)

counter_lock = Lock()
counter = 0


def log_movie_to_account(user_id, username, tconst, movie_data, db_config):
    logging.info("Entered log_movie_to_account function.")
    poster_url = movie_data.get('poster_url', None)
    logging.info(f"Trying to log tconst: {tconst} with poster URL: {poster_url} for user ID: {user_id}")

    if not poster_url:
        logging.warning("Poster URL is NULL. Using a placeholder.")
        poster_url = "placeholder_url"

    watched_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO watched_movies (user_id, tconst, watched_at, username, poster_url) VALUES (%s, %s, %s, %s, %s)"
    execute_query(db_config, query, (user_id, tconst, watched_at, username, poster_url), fetch='none')
    logging.info(f"Successfully logged movie {tconst} for user {user_id}.")

    insert_query = """
        INSERT INTO watched_movie_detail (user_id, tconst, title, genres, directors, writers, runtimes, rating, votes, poster_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        user_id, tconst, movie_data['title'], movie_data['genres'], movie_data['directors'], movie_data['writers'],
        movie_data['runtimes'], movie_data['rating'], movie_data['votes'], poster_url
    )
    execute_query(user_db_config, insert_query, values, fetch='none')
    logging.info(f"Data for tconst {tconst} inserted successfully.")


def query_watched_movie(user_id, tconst, db_config):
    query = "SELECT * FROM watched_movies WHERE user_id=%s AND tconst=%s"
    return execute_query(db_config, query, (user_id, tconst))


def update_title_basics_if_empty(tconst, plot, poster_url, db_config):
    query = "SELECT plot, poster_url FROM `title.basics` WHERE tconst=%s;"
    result = execute_query(db_config, query, (tconst,), fetch='one')
    if result and (result['plot'] is None or result['poster_url'] is None):
        update_query = """
        UPDATE `title.basics`
        SET plot = %s, poster_url = %s
        WHERE tconst = %s;
        """
        execute_query(db_config, update_query, (plot, poster_url, tconst), fetch='none')
        return True
    return False


def fetch_and_update_movie(row, db_config):
    global counter
    tconst = row['tconst']
    logging.info(f"Fetching information for {tconst}...")

    movie = fetch_movie_info_from_imdb(tconst)
    plot = movie.get('plot outline')
    poster_url = movie.get('cover url')
    is_updated = update_title_basics_if_empty(tconst, plot, poster_url, db_config)
    if is_updated:
        with counter_lock:
            counter += 1
            print(counter)


def update_missing_title_info(db_config, start_tconst=None):
    global counter
    counter = 0

    query = """
    SELECT tconst
    FROM `title.basics`
    WHERE plot IS NULL
    AND poster_url IS NULL
    AND titleType = 'movie'
    """

    # If a start_tconst is specified, add a condition for it
    if start_tconst is not None:
        query += f" AND tconst > '{start_tconst}'"

    query += " LIMIT 10000;"

    result = execute_query(db_config, query, fetch='all')

    if not result:
        logging.info("No records need updating.")
        return

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(fetch_and_update_movie, result, [db_config] * len(result))

    logging.info(f"Updated {counter} rows.")


# Initialize logging
logging.basicConfig(level=logging.INFO)


# Function to add a movie to a user's watchlist
def add_movie_to_watchlist(user_id, username, tconst, movie_data, db_config):
    """
    Adds a movie to a user's watchlist in the database.

    Parameters:
    user_id (int): The ID of the user.
    username (str): The username of the user.
    tconst (str): The IMDb ID of the movie.
    movie_data (dict): A dictionary containing detailed information about the movie.
    db_config (dict): Database configuration.
    """
    # Log the entry into the function
    logging.info("Entered add_movie_to_watchlist function.")

    # Extract the poster URL from the movie_data dictionary
    poster_url = movie_data.get('poster_url', None)

    # Log what movie is being added and for which user
    logging.info(
        f"Trying to add tconst: {tconst} with poster URL: {poster_url} to watchlist for user ID: {user_id}, Username: {username}")

    # Handle case where poster_url is not available
    if not poster_url:
        logging.warning("Poster URL is NULL. Using a placeholder.")
        poster_url = "placeholder_url"

    # Get the current timestamp
    added_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insert the main record into the user_watchlist table
    query = "INSERT INTO user_watchlist (user_id, tconst, added_at, username, poster_url) VALUES (%s, %s, %s, %s, %s)"
    execute_query(db_config, query, (user_id, tconst, added_at, username, poster_url), fetch='none')
    logging.info(f"Successfully added movie {tconst} to watchlist for user {user_id}.")

    # Insert additional movie details into the user_watchlist_detail table
    insert_query = """
        INSERT INTO user_watchlist_detail (user_id, tconst, title, genres, directors, writers, runtimes, rating, votes, poster_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        user_id, tconst, movie_data['title'], movie_data['genres'], movie_data['directors'], movie_data['writers'],
        movie_data['runtimes'], movie_data['rating'], movie_data['votes'], poster_url
    )
    execute_query(db_config, insert_query, values, fetch='none')

    # Log that the additional details have been successfully inserted
    logging.info(f"Data for tconst {tconst} inserted successfully into user_watchlist_detail.")


# Execute the function to update missing information
# update_missing_title_info(db_config, start_tconst='tt0353347')
