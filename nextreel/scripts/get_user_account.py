import imdb
import pymysql

from nextreel.scripts.mysql_query_builder import execute_query
from nextreel.scripts.db_config_scripts import user_db_config, db_config  # Import both configs


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

    poster_data = []

    # SQL query to fetch poster URLs and tconst for the specific user
    sql_query = "SELECT poster_url, tconst FROM watched_movies WHERE user_id = %s"

    # Execute the query
    results = execute_query(db_config, sql_query, params=(user_id,), fetch='all')

    # Extract poster URLs and tconst from query results
    for row in results:
        poster_data.append({
            'url': row['poster_url'],
            'tconst': row['tconst']
        })
        # print(f"Fetched poster URL: {row['poster_url']} for tconst: {row['tconst']}")  # Debugging line

    return poster_data


def get_watched_movies(user_id, db_config):
    print("Entered get_watched_movies function.")  # Debugging line

    watched_movies = []

    # SQL query to fetch poster URLs for the specific user
    sql_query = "SELECT tconst FROM watched_movies WHERE user_id = %s"

    # Execute the query
    results = execute_query(db_config, sql_query, params=(user_id,), fetch='all')

    # Extract poster URLs from query results
    for row in results:
        watched_movies.append(row['tconst'])
        print(f"Fetched tconst: {row['tconst']}")  # Debugging line

    return watched_movies


def get_all_watched_movie_details_by_user(user_id):
    print("Entered get_all_watched_movie_details_by_user function.")  # Debugging line

    query = """
    SELECT * FROM watched_movie_detail 
    WHERE user_id=%s;
    """

    rows = execute_query(user_db_config, query, (user_id,), fetch='all')

    all_movie_details = []

    for row in rows:
        # Map each row onto a dictionary
        mapped_data = {
            'tconst': row['tconst'],
            'title': row['title'],
            'genres': row['genres'],
            'directors': row['directors'],
            'writers': row['writers'],
            'runtimes': row['runtimes'],
            'rating': row['rating'],
            'votes': row['votes'],
            'poster_url': row['poster_url']  # Add this line
        }
        all_movie_details.append(mapped_data)

    return all_movie_details


def get_watched_movie_details(user_id, tconst):
    # Step 1: Fetch relevant IMDb data using db_config
    imdb_query = """
    SELECT 
    `title.basics`.primaryTitle AS title,
    `title.basics`.genres,
    `title.crew`.directors,
    `title.crew`.writers,
    `title.basics`.runtimeMinutes AS runtimes,
    `title.ratings`.averageRating AS rating,
    `title.ratings`.numVotes AS votes
FROM 
    `title.basics`
JOIN
    `title.ratings` ON `title.basics`.tconst = `title.ratings`.tconst
JOIN
    `title.crew` ON `title.basics`.tconst = `title.crew`.tconst
WHERE 
    `title.basics`.tconst = %s;
    """
    imdb_data = execute_query(db_config, imdb_query, tconst, fetch='all')
    return imdb_data


def insert_watched_movie_details(user_id, tconst, imdb_data, poster_url):
    print("Entered insert_watched_movie_details function.")  # Debugging line
    insert_query = """
    INSERT INTO watched_movie_detail (user_id, tconst, title, genres, directors, writers, runtimes, rating, votes, poster_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        user_id, tconst, imdb_data['title'], imdb_data['genres'], imdb_data['directors'], imdb_data['writers'],
        imdb_data['runtimes'], imdb_data['rating'], imdb_data['votes'], poster_url
    )
    execute_query(user_db_config, insert_query, values, fetch='none')
    print(f"Data for tconst {tconst} inserted successfully.")  # Debugging line


def get_all_movies_in_watchlist(user_id):
    # Debugging line to indicate entry into function
    print("Entered get_all_movies_in_watchlist function.")

    # SQL query to fetch all movies from the user's watchlist
    query = "SELECT * FROM user_watchlist_detail WHERE user_id=%s"

    # Execute the query
    watchlist_movies = execute_query(user_db_config, query, params=(user_id,), fetch='all')

    if watchlist_movies:
        print(f"Fetched {len(watchlist_movies)} movies from watchlist for user {user_id}.")  # Debugging line
    else:
        print(f"No movies found in the watchlist for user {user_id}.")  # Debugging line

    return watchlist_movies


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
