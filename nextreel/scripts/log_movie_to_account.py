import json
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
import logging
from threading import Lock

import imdb

from nextreel.scripts.db_config_scripts import user_db_config
from nextreel.scripts.movie import Movie
from nextreel.scripts.mysql_query_builder import execute_query, QUERY_WATCHED_MOVIE, SELECT_MISSING_TITLE_INFO, \
    ADD_MOVIE_TO_WATCHLIST, INSERT_WATCHED_MOVIE_DETAIL, INSERT_USER_WATCHLIST_DETAIL, LOG_MOVIE_TO_ACCOUNT, \
    CHECK_TITLE_BASICS

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
    execute_query(db_config, LOG_MOVIE_TO_ACCOUNT, (user_id, tconst, watched_at, username, poster_url), fetch='none'),

    logging.info(f"Successfully logged movie {tconst} for user {user_id}.")

    values = (
        user_id, tconst, movie_data['title'], movie_data['genres'], movie_data['directors'], movie_data['writers'],
        movie_data['runtimes'], movie_data['rating'], movie_data['votes'], poster_url
    )
    execute_query(user_db_config, INSERT_WATCHED_MOVIE_DETAIL, values, fetch='none')

    logging.info(f"Data for tconst {tconst} inserted successfully.")


def query_watched_movie(user_id, tconst, db_config):
    return execute_query(db_config, QUERY_WATCHED_MOVIE, (user_id, tconst))


def update_title_basics_if_empty(tconst, plot, poster_url, fetched_languages, db_config):
    """
    Updates the title.basics table with new data if existing fields are empty.

    Parameters:
    tconst (str): The IMDb ID of the movie.
    plot (str): The plot summary of the movie.
    poster_url (str): The URL of the movie poster.
    fetched_languages (list or str): The languages in which the movie is available.
    db_config (dict): Database configuration.

    Returns:
    bool: True if any fields were updated, False otherwise.
    """
    # Query to check existing data for the given tconst
    query = "SELECT plot, poster_url, language FROM `title.basics` WHERE tconst=%s;"
    result = execute_query(db_config, CHECK_TITLE_BASICS, (tconst,), fetch='one')

    # Initialize flags to determine which fields need to be updated
    update_plot = False
    update_poster_url = False
    update_language = False

    # Check if plot, poster_url, or language are empty and need to be updated
    if result:
        if result['plot'] is None:
            update_plot = True
        if result['poster_url'] is None:
            update_poster_url = True
        if result['language'] is None:
            update_language = True
        else:
            # Additional check to see if fetched language is different from stored language
            stored_languages = result['language'].split(', ')
            if fetched_languages and fetched_languages[0] != stored_languages[0]:
                update_language = True

        # Before updating, ensure fetched_languages is properly formatted
        if fetched_languages and isinstance(fetched_languages, list):
            fetched_languages_str = ', '.join(fetched_languages)  # Convert list to comma-separated string
        elif fetched_languages and isinstance(fetched_languages, str):
            # Remove any unwanted characters like commas or spaces
            fetched_languages_str = fetched_languages.replace(", ", "").replace(",", "")
        else:
            fetched_languages_str = None

        # Update the database fields if any of them need to be updated
        if update_plot or update_poster_url or update_language:
            update_query = """
            UPDATE `title.basics`
            SET plot = %s, poster_url = %s, language = %s
            WHERE tconst = %s;
            """
            execute_query(db_config, update_query, (
                plot if update_plot else result['plot'],
                poster_url if update_poster_url else result['poster_url'],
                fetched_languages_str if update_language else result['language'],
                tconst), fetch='none')
            return True  # Return True to indicate that an update was made
    return False  # Return False if no update was needed


# Function is updated to fetch 'language' from IMDb
def fetch_and_update_movie(row, db_config):
    global counter
    tconst = row['tconst']
    logging.info(f"Fetching information for {tconst}...")

    movie = Movie.fetch_info_from_imdb(tconst)
    plot = movie.get('plot outline')
    poster_url = movie.get('cover url')
    language = movie.get('languages')  # Assuming 'languages' returns a list

    is_updated = update_title_basics_if_empty(tconst, plot, poster_url, language, db_config)
    if is_updated:
        with counter_lock:
            counter += 1
            print(counter)


def update_missing_title_info(db_config, start_tconst=None):
    global counter
    counter = 0
    query = SELECT_MISSING_TITLE_INFO
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
    execute_query(db_config, ADD_MOVIE_TO_WATCHLIST, (user_id, tconst, added_at, username, poster_url), fetch='none')

    logging.info(f"Successfully added movie {tconst} to watchlist for user {user_id}.")

    # Insert additional movie details into the user_watchlist_detail table

    values = (
        user_id, tconst, movie_data['title'], movie_data['genres'], movie_data['directors'], movie_data['writers'],
        movie_data['runtimes'], movie_data['rating'], movie_data['votes'], poster_url
    )
    execute_query(db_config, INSERT_USER_WATCHLIST_DETAIL, values, fetch='none')

    # Log that the additional details have been successfully inserted
    logging.info(f"Data for tconst {tconst} inserted successfully into user_watchlist_detail.")

# Execute the function to update missing information
# update_missing_title_info(db_config, start_tconst='tt0353347')
