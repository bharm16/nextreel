import random
import time

import pymysql
import imdb
import random
import pymysql
import imdb

import sys

from nextreel.scripts.mysql_query_builder import execute_query

print("Python Executable:", sys.executable)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}


def get_db_connection(db_config):
    """Establish a connection to the database."""
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )


def get_random_row_value(db_config, table_name, column_name):
    count_query = f"SELECT COUNT(*) FROM `{table_name}`"
    total_rows = execute_query(db_config, count_query)[0][0]

    random_row_num = random.randint(1, total_rows)

    value_query = f"SELECT {column_name} FROM `{table_name}` LIMIT %s, 1"
    random_value = execute_query(db_config, value_query, (random_row_num - 1,))[0][0]

    row_query = f"SELECT * FROM `{table_name}` WHERE {column_name} = %s"
    random_row = execute_query(db_config, row_query, (random_value,))

    return random_row


def get_filtered_random_row(db_config, criteria):
    min_year = criteria.get('min_year', 2000)
    max_year = criteria.get('max_year', 2020)
    min_rating = criteria.get('min_rating', 7.5)
    max_rating = criteria.get('max_rating', 10)
    min_votes = criteria.get('min_votes', 100000)
    title_type = criteria.get('title_type', 'movie')
    genres = criteria.get('genres')

    parameters = [min_year, max_year, min_rating, max_rating, min_votes, title_type]

    genre_conditions = ["tb.genres LIKE %s" for _ in genres] if genres else []

    query = """
    SELECT tb.*
    FROM `title.basics` tb
    JOIN `title.ratings` tr ON tb.tconst = tr.tconst
    WHERE tb.startYear >= %s AND tb.startYear <= %s
    AND tr.averagerating >= %s AND tr.averagerating <= %s
    AND tr.numVotes >= %s
    AND tb.titleType = %s
    """ + (" AND (" + " OR ".join(genre_conditions) + ")" if genres else "") + " ORDER BY RAND() LIMIT 1"

    if genres:
        parameters.extend(["%" + genre + "%" for genre in genres])

    print("Generated SQL Query:", query)
    print("Query Parameters:", parameters)

    random_row = execute_query(db_config, query, parameters)
    return random_row if random_row else None


def fetch_movie_info_from_imdb(tconst):
    imdbId = int(tconst[2:])
    ia = imdb.IMDb()
    return ia.get_movie(imdbId)


def main(criteria):
    row = get_filtered_random_row(db_config, criteria)
    if not row:
        print("No movies found based on the given criteria.")
        return None

    # Record the start time
    start_time = time.time()

    # Call the function
    movie_info = fetch_movie_info_from_imdb(row['tconst'])

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the elapsed time
    print(f"Time taken by fetch_movie_info_from_imdb: {elapsed_time} seconds")

    return movie_info


if __name__ == "__main__":
    criteria = {
        "min_year": 2000,
        "max_year": 2020,
        "min_rating": 7.5,
        "max_rating": 10,
        "title_type": "movie",
        "genres": ["Action", "Drama"]
    }
    main(criteria)
