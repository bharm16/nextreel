import imdb

from nextreel.scripts.mysql_query_builder import execute_query
from nextreel.scripts.db_config_scripts import user_db_config
from nextreel.scripts.getMovieFromIMDB import fetch_movie_info_from_imdb


def get_user_by_id(user_id):
    return execute_query(user_db_config, "SELECT * FROM users WHERE id=%s", (user_id,))


def get_user_by_username(username):
    return execute_query(user_db_config, "SELECT * FROM users WHERE username=%s", (username,))


def get_all_users():
    return execute_query(user_db_config, "SELECT * FROM users", fetch='all')


def insert_new_user(username, email, password):
    existing_user = execute_query(user_db_config, "SELECT * FROM users WHERE username=%s", (username,))
    if existing_user:
        return "Username already exists."

    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    execute_query(user_db_config, query, (username, email, password), fetch='none')

    # If you need the newly created user ID, you'd need to execute another query to fetch it.
    new_user = execute_query(user_db_config, "SELECT * FROM users WHERE username=%s", (username,))

    return {"message": f"User created successfully with ID {new_user['id']}.", "id": new_user['id']}


# def get_watched_movies_and_posters(current_user, user_db_config):
#     ia = imdb.IMDb()
#     watched_movie_tconst = []
#     watched_movie_posters = []
#
#     # Query to get the watched movies for the current user
#     watched_movies_query = "SELECT tconst FROM watched_movies WHERE username = %s"
#     watched_movies = execute_query(user_db_config, watched_movies_query, (current_user.username,), fetch='all')
#
#     for row in watched_movies:
#         watched_movie_tconst.append(row['tconst'])
#
#     for tconst in watched_movie_tconst:
#         movie = fetch_movie_info_from_imdb(tconst)
#         movie_poster = movie.get_fullsizeURL()
#         watched_movie_posters.append(movie_poster)
#         print(watched_movie_posters)
#
#     return watched_movie_tconst, watched_movie_posters


def get_watched_movie_posters(user, db_config):
    user_id = user.id  # Assuming the user object has an 'id' attribute
    poster_urls = []

    # SQL query to fetch poster URLs for the specific user
    sql_query = "SELECT poster_url FROM watched_movies WHERE user_id = %s"

    # Execute the query
    results = execute_query(db_config, sql_query, params=(user_id,), fetch='all')

    # Extract poster URLs from query results
    for row in results:
        poster_urls.append(row['poster_url'])

    return poster_urls

# Example usage
if __name__ == "__main__":
    user_by_id = get_user_by_id(1)
    print("User with ID 1:", user_by_id)

    user_by_username = get_user_by_username('john_doe')
    print("User with username 'john_doe':", user_by_username)

    all_users = get_all_users()
    print("All users:")
    for user in all_users:
        print(user)
