from datetime import datetime
import logging
import imdb

from nextreel.scripts.db_config_scripts import user_db_config, db_config  # Import both configs
from nextreel.scripts.getMovieFromIMDB import fetch_movie_info_from_imdb
from nextreel.scripts.mysql_query_builder import execute_query

# Initialize logging
logging.basicConfig(level=logging.INFO)


def log_movie_to_account(user_id, username, tconst, movie_data, db_config):
    logging.info("Entered log_movie_to_account function.")

    poster_url = movie_data.get('poster_url', None)  # Get the poster URL from the movie_data
    logging.info(f"Trying to log tconst: {tconst} with poster URL: {poster_url} for user ID: {user_id}")

    if not poster_url:
        logging.warning("Poster URL is NULL. Using a placeholder.")
        poster_url = "placeholder_url"

    watched_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO watched_movies (user_id, tconst, watched_at, username, poster_url) VALUES (%s, %s, %s, %s, %s)"
    execute_query(db_config, query, (user_id, tconst, watched_at, username, poster_url), fetch='none')
    logging.info(f"Successfully logged movie {tconst} for user {user_id}.")

    # Insert watched_movie_details logic here
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


# except Exception as e:
#     logging.error(f"Error: {e}")
#     raise e

def query_watched_movie(user_id, tconst, db_config):
    query = "SELECT * FROM watched_movies WHERE user_id=%s AND tconst=%s"
    return execute_query(db_config, query, (user_id, tconst))


def update_title_basics_if_empty(tconst, plot, poster_url, db_config):
    # First, check if the plot and poster_url already exist for the given tconst
    query = "SELECT plot, poster_url FROM `title.basics` WHERE tconst=%s;"
    result = execute_query(db_config, query, (tconst,), fetch='one')

    # If plot and poster_url are None, then update them
    if result and (result['plot'] is None or result['poster_url'] is None):
        update_query = """
        UPDATE `title.basics`
        SET plot = %s, poster_url = %s
        WHERE tconst = %s;
        """
        execute_query(db_config, update_query, (plot, poster_url, tconst), fetch='none')


def update_missing_title_info(db_config):
    # Step 1: Retrieve up to 100 tconst values where either plot or poster_url is empty
    query = """
    SELECT tconst 
    FROM `title.basics`
    WHERE plot IS NULL
    AND poster_url IS NULL
    AND titleType = 'movie'
    LIMIT 100;
    """
    result = execute_query(db_config, query, fetch='all')

    if not result:
        print("No records need updating.")
        return

    # Step 2 and 3: Loop through the tconst values, fetch from IMDb, and update
    for row in result:
        tconst = row['tconst']

        print(f"Fetching information for {tconst}...")

        # Fetch from IMDb
        movie = fetch_movie_info_from_imdb(tconst)
        plot = movie.get('plot outline')  # Assuming 'plot outline' is the key for plot
        poster_url = movie.get('cover url')  # Assuming 'cover url' is the key for poster URL

        # Update the title.basics table
        update_title_basics_if_empty(tconst, plot, poster_url, db_config)


# Now you can call this function to update up to 100 missing information
update_missing_title_info(db_config)

# if __name__ == "__main__":
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'caching_sha2_password',
#     'db': 'UserAccounts'
# }
#
# user_id = 'test_user'
# tconst = 'test_tconst'
#
# # Log the movie to the account and print output
# log_movie_to_account(user_id, tconst, db_config)
#
# # Query the database to see if the movie was logged
# result = query_watched_movie(user_id, tconst, db_config)
#
# # Validate that the row exists using print statements
# if result:
#     print("The movie has been successfully logged into the database.")
#     print(f"User ID: {result['user_id']}")
#     print(f"tconst: {result['tconst']}")
#     print(f"Watched At: {result['watched_at']}")
# else:
#     print("The movie was not logged into the database.")
