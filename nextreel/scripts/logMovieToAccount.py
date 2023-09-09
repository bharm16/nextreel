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

    # try:
    execute_query(db_config, query, (user_id, tconst, watched_at, username, poster_url), fetch='none')
    logging.info(f"Successfully logged movie {tconst} for user {user_id}.")

    # Insert watched_movie_details logic here
    insert_query = """
        INSERT INTO watched_movie_detail (user_id, tconst, title, genres, directors, writers, runtimes, rating, votes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    values = (
        user_id, tconst, movie_data['title'], movie_data['genres'], movie_data['directors'], movie_data['writers'],
        movie_data['runtimes'], movie_data['rating'], movie_data['votes']
    )
    execute_query(user_db_config, insert_query, (
        user_id, tconst, movie_data['title'], movie_data['genres'], movie_data['directors'], movie_data['writers'],
        movie_data['runtimes'], movie_data['rating'], movie_data['votes']
    ), fetch='none')
    logging.info(f"Data for tconst {tconst} inserted successfully.")


# except Exception as e:
#     logging.error(f"Error: {e}")
#     raise e

def query_watched_movie(user_id, tconst, db_config):
    query = "SELECT * FROM watched_movies WHERE user_id=%s AND tconst=%s"
    return execute_query(db_config, query, (user_id, tconst))

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
