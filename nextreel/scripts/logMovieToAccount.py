import pymysql
from datetime import datetime

def log_movie_to_account(user_id, tconst, db_config):
    print(f"Logging movie {tconst} for user {user_id}")  # Debugging line

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        watched_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO watched_movies (user_id, tconst, watched_at) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, tconst, watched_at))
        conn.commit()
        print(f"Successfully logged movie {tconst} for user {user_id}.")
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def query_watched_movie(user_id, tconst, db_config):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM watched_movies WHERE user_id=%s AND tconst=%s"
        cursor.execute(query, (user_id, tconst))
        result = cursor.fetchone()
        return result
    finally:
        cursor.close()
        conn.close()

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
