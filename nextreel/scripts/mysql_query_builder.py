# queries.py
import time

import pymysql

# Query to fetch user details based on the username
GET_USER_BY_USERNAME = "SELECT * FROM users WHERE username=%s"

# Query to fetch user details by ID
GET_USER_BY_ID = "SELECT * FROM users WHERE id=%s"

# Query to fetch all users
GET_ALL_USERS = "SELECT * FROM users"

# Query to insert a new user
INSERT_NEW_USER = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"

# Query to fetch watched movie posters for a user
GET_WATCHED_MOVIE_POSTERS = "SELECT poster_url, tconst FROM watched_movies WHERE user_id = %s"

# Query to fetch watched movies for a user
GET_WATCHED_MOVIES = "SELECT tconst FROM watched_movies WHERE user_id = %s"

# Query to fetch all watched movie details for a user
GET_ALL_WATCHED_MOVIE_DETAILS = """
SELECT * FROM watched_movie_detail 
WHERE user_id=%s;
"""

# Query to fetch IMDb details of a watched movie
GET_WATCHED_MOVIE_DETAILS = """
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

# Query to fetch all movies in a user's watchlist
GET_ALL_MOVIES_IN_WATCHLIST = "SELECT * FROM user_watchlist_detail WHERE user_id=%s"

GET_ALL_WATCHED_MOVIE_DETAILS_BY_USER = """
SELECT * FROM watched_movie_detail 
WHERE user_id=%s;
"""


def execute_query(db_config, query, params=None, fetch='one'):
    start_time = time.time()  # Start the timer

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(query, params)

    if fetch == 'one':
        result = cursor.fetchone()
    elif fetch == 'all':
        result = cursor.fetchall()
    elif fetch == 'none':  # For queries like INSERT, UPDATE, DELETE
        conn.commit()
        result = None

    end_time = time.time()  # Stop the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time

    # print(f"Execution time for query: {elapsed_time:.5f} seconds")

    cursor.close()
    conn.close()
    return result


def get_db_connection(db_config):
    """Establish a connection to the database."""
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )