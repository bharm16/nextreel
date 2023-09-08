from datetime import datetime

import imdb

from nextreel.scripts.db_config_scripts import user_db_config
from nextreel.scripts.getMovieFromIMDB import fetch_movie_info_from_imdb
from nextreel.scripts.mysql_query_builder import execute_query


def log_movie_to_account(user_id, tconst, db_config):
    print(f"Logging movie {tconst} for user {user_id}")  # Debugging line

    watched_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO watched_movies (user_id, tconst, watched_at) VALUES (%s, %s, %s)"

    ia = imdb.IMDb()

    movie = fetch_movie_info_from_imdb(tconst)
    movie_poster = movie.get_fullsizeURL()



    # Insert the movie and its poster URL into the watched_movies table
    insert_query = "INSERT INTO watched_movies (username, tconst, poster_url) VALUES (%s, %s, %s)"
    execute_query(user_db_config, insert_query, (user_id, tconst, movie_poster))



    try:
        execute_query(db_config, query, (user_id, tconst, watched_at), fetch='none')
        print(f"Successfully logged movie {tconst} for user {user_id}.")
    except Exception as e:
        print(f"Error: {e}")
        raise e


def query_watched_movie(user_id, tconst, db_config):
    query = "SELECT * FROM watched_movies WHERE user_id=%s AND tconst=%s"
    return execute_query(db_config, query, (user_id, tconst))


if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'caching_sha2_password',
        'db': 'UserAccounts'
    }

    user_id = 'test_user'
    tconst = 'test_tconst'

    # Log the movie to the account and print output
    log_movie_to_account(user_id, tconst, db_config)

    # Query the database to see if the movie was logged
    result = query_watched_movie(user_id, tconst, db_config)

    # Validate that the row exists using print statements
    if result:
        print("The movie has been successfully logged into the database.")
        print(f"User ID: {result['user_id']}")
        print(f"tconst: {result['tconst']}")
        print(f"Watched At: {result['watched_at']}")
    else:
        print("The movie was not logged into the database.")
