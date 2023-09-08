import imdb

from nextreel.scripts.mysql_query_builder import execute_query
from nextreel.scripts.db_config_scripts import user_db_config


def get_user_by_id(user_id):
    print("Entered get_user_by_id function.")  # Debugging line
    return execute_query(user_db_config, "SELECT * FROM users WHERE id=%s", (user_id,))


def get_user_by_username(username):
    print("Entered get_user_by_username function.")  # Debugging line
    return execute_query(user_db_config, "SELECT * FROM users WHERE username=%s", (username,))


def get_all_users():
    print("Entered get_all_users function.")  # Debugging line
    return execute_query(user_db_config, "SELECT * FROM users", fetch='all')


def insert_new_user(username, email, password):
    print("Entered insert_new_user function.")  # Debugging line

    existing_user = execute_query(user_db_config, "SELECT * FROM users WHERE username=%s", (username,))
    if existing_user:
        print("Username already exists.")  # Debugging line
        return "Username already exists."

    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    execute_query(user_db_config, query, (username, email, password), fetch='none')

    new_user = execute_query(user_db_config, "SELECT * FROM users WHERE username=%s", (username,))
    print(f"User created successfully with ID {new_user['id']}.")  # Debugging line

    return {"message": f"User created successfully with ID {new_user['id']}.", "id": new_user['id']}


def get_watched_movie_posters(user_id, db_config):
    print("Entered get_watched_movie_posters function.")  # Debugging line

    poster_urls = []

    # SQL query to fetch poster URLs for the specific user
    sql_query = "SELECT poster_url FROM watched_movies WHERE user_id = %s"

    # Execute the query
    results = execute_query(db_config, sql_query, params=(user_id,), fetch='all')

    # Extract poster URLs from query results
    for row in results:
        poster_urls.append(row['poster_url'])
        print(f"Fetched poster URL: {row['poster_url']}")  # Debugging line

    return poster_urls


# Example usage
if __name__ == "__main__":
    print("Script started.")  # Debugging line

    user_by_id = get_user_by_id(1)
    print(f"User with ID 1: {user_by_id}")  # Debugging line

    user_by_username = get_user_by_username('john_doe')
    print(f"User with username 'john_doe': {user_by_username}")  # Debugging line

    all_users = get_all_users()
    print("All users:")  # Debugging line
    for user in all_users:
        print(user)
