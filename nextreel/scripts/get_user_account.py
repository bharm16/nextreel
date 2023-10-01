import imdb
import pymysql

from nextreel.scripts.mysql_query_builder import execute_query, GET_USER_BY_USERNAME, GET_USER_BY_ID, \
    GET_WATCHED_MOVIE_DETAILS, GET_ALL_WATCHED_MOVIE_DETAILS_BY_USER, INSERT_NEW_USER, GET_ALL_USERS, \
    GET_WATCHED_MOVIE_POSTERS, GET_WATCHED_MOVIES, GET_ALL_MOVIES_IN_WATCHLIST
from nextreel.scripts.db_config_scripts import user_db_config, db_config  # Import both configs


def get_user_login(username, password, db_config):
    user_data = execute_query(db_config, GET_USER_BY_USERNAME, (username,))
    if user_data and user_data['password'] == password:
        return user_data
    else:
        return None


def get_user_by_id(user_id):
    return execute_query(user_db_config, GET_USER_BY_ID, (user_id,))


def get_user_by_username(username):
    return execute_query(user_db_config, GET_USER_BY_USERNAME, (username,))


def get_all_users():
    return execute_query(user_db_config, GET_ALL_USERS, fetch='all')


def insert_new_user(username, email, password):
    existing_user = execute_query(user_db_config, GET_USER_BY_USERNAME, (username,))
    if existing_user:
        return "Username already exists."
    execute_query(user_db_config, INSERT_NEW_USER, (username, email, password), fetch='none')
    new_user = execute_query(user_db_config, GET_USER_BY_USERNAME, (username,))
    return {"message": f"User created successfully with ID {new_user['id']}.", "id": new_user['id']}


def transform_poster_data(row):
    return {'url': row['poster_url'], 'tconst': row['tconst']}


# Helper function to transform watched movies data
def transform_watched_movies(row):
    return row['tconst']


def get_watched_movie_posters(user_id, db_config):
    print("Entered get_watched_movie_posters function.")
    rows = execute_query(db_config, GET_WATCHED_MOVIE_POSTERS, params=(user_id,), fetch='all')
    return [transform_poster_data(row) for row in rows]


def get_watched_movies(user_id, db_config):
    print("Entered get_watched_movies function.")
    rows = execute_query(db_config, GET_WATCHED_MOVIES, params=(user_id,), fetch='all')
    return [transform_watched_movies(row) for row in rows]


def transform_movie_details(row):
    """
    Helper function to transform a SQL row into a dictionary
    """
    return {
        'tconst': row['tconst'],
        'title': row['title'],
        'genres': row['genres'],
        'directors': row['directors'],
        'writers': row['writers'],
        'runtimes': row['runtimes'],
        'rating': row['rating'],
        'votes': row['votes'],
        'poster_url': row['poster_url']
    }


def get_all_watched_movie_details_by_user(user_id):
    all_movie_details = []
    rows = execute_query(user_db_config, GET_ALL_WATCHED_MOVIE_DETAILS_BY_USER, (user_id,), fetch='all')
    for row in rows:
        all_movie_details.append(transform_movie_details(row))
    return all_movie_details  # Make sure to return the list




def get_watched_movie_details(tconst):
    imdb_data = execute_query(db_config, GET_WATCHED_MOVIE_DETAILS, (tconst,), fetch='all')
    return imdb_data  # Consider further transformation if necessary


def get_all_movies_in_watchlist(user_id):
    print("Entered get_all_movies_in_watchlist function.")  # Debugging line

    # Execute the query
    rows = execute_query(user_db_config, GET_ALL_MOVIES_IN_WATCHLIST, params=(user_id,), fetch='all')

    # Transform the fetched rows using the helper function
    return [transform_movie_details(row) for row in rows]


# Example usage
if __name__ == "__main__":
    print("Script started.")  # Debugging line

    user_by_id = get_user_by_id(17)
    print(f"User with ID 1: {user_by_id}")  # Debugging line

    user_by_username = get_user_by_username('john_doe')
    print(f"User with username 'john_doe': {user_by_username}")  # Debugging line

    all_users = get_all_users()
    print("All users:")  # Debugging line
    for user in all_users:
        print(user)
