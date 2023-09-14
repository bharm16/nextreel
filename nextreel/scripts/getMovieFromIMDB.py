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
    """Fetch a random row's value from a specific table and column."""
    # SQL query to get the total number of rows in the table
    count_query = f"SELECT COUNT(*) FROM `{table_name}`"
    # Execute the query and get the total number of rows
    total_rows = execute_query(db_config, count_query)[0][0]
    # Generate a random row number
    random_row_num = random.randint(1, total_rows)
    # SQL query to get a specific column value from the randomly chosen row
    value_query = f"SELECT {column_name} FROM `{table_name}` LIMIT %s, 1"
    # Execute the query and get the value
    random_value = execute_query(db_config, value_query, (random_row_num - 1,))[0][0]
    # SQL query to get the entire row where the column has the random value
    row_query = f"SELECT * FROM `{table_name}` WHERE {column_name} = %s"
    # Execute the query and get the row
    random_row = execute_query(db_config, row_query, (random_value,))
    return random_row


# def get_filtered_random_row(db_config, criteria):
#     min_year = criteria.get('min_year', 1900)
#     max_year = criteria.get('max_year', 2023)
#     min_rating = criteria.get('min_rating', 7.0)
#     max_rating = criteria.get('max_rating', 10)
#     min_votes = criteria.get('min_votes', 100000)
#     title_type = criteria.get('title_type', 'movie')
#     genres = criteria.get('genres')
#
#     parameters = [min_year, max_year, min_rating, max_rating, min_votes, title_type]
#
#     genre_conditions = ["tb.genres LIKE %s" for _ in genres] if genres else []
#
#     query = """
#     SELECT tb.*
#     FROM `title.basics` tb
#     JOIN `title.ratings` tr ON tb.tconst = tr.tconst
#     WHERE tb.startYear >= %s AND tb.startYear <= %s
#     AND tr.averagerating >= %s AND tr.averagerating <= %s
#     AND tr.numVotes >= %s
#     AND tb.titleType = %s
#     """ + (" AND (" + " OR ".join(genre_conditions) + ")" if genres else "") + " ORDER BY RAND() LIMIT 1"
#
#     if genres:
#         parameters.extend(["%" + genre + "%" for genre in genres])
#
#     print("Generated SQL Query:", query)
#     print("Query Parameters:", parameters)
#
#     random_row = execute_query(db_config, query, parameters)
#     return random_row if random_row else None


def get_filtered_random_row(db_config, criteria):
    min_year = criteria.get('min_year', 1900)
    max_year = criteria.get('max_year', 2023)
    min_rating = criteria.get('min_rating', 7.0)
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
    JOIN `title.akas` ta ON tb.tconst = ta.titleId
    WHERE tb.startYear >= %s AND tb.startYear <= %s
    AND tr.averagerating >= %s AND tr.averagerating <= %s
    AND tr.numVotes >= %s
    AND tb.titleType = %s
    AND ta.language = 'en'
    """ + (" AND (" + " OR ".join(genre_conditions) + ")" if genres else "") + " ORDER BY RAND() LIMIT 1"

    if genres:
        parameters.extend(["%" + genre + "%" for genre in genres])

    print("Generated SQL Query:", query)
    print("Query Parameters:", parameters)

    random_row = execute_query(db_config, query, parameters)
    print(random_row)

    return random_row if random_row else None



def fetch_movie_info_from_imdb(tconst):
    """Fetch movie information from IMDb using IMDbPY."""
    # Convert tconst to IMDb ID (integer)
    imdbId = int(tconst[2:])
    # Create an IMDb object
    ia = imdb.IMDb()
    # Fetch and return the movie information
    return ia.get_movie(imdbId)


def main(criteria):
    """Main function to execute the program."""
    # Fetch a random movie row that matches the criteria
    row = get_filtered_random_row(db_config, criteria)
    if not row:
        print("No movies found based on the given criteria.")
        return None

    # Record the start time for fetching movie info
    start_time = time.time()

    # Fetch movie info from IMDb
    movie_info = fetch_movie_info_from_imdb(row['tconst'])

    # Record the end time for fetching movie info
    end_time = time.time()

    print("Fetched movie genres:", movie_info.get('genres'))

    # Calculate and print the time taken to fetch movie info
    elapsed_time = end_time - start_time
    print(f"Time taken by fetch_movie_info_from_imdb: {elapsed_time} seconds")

    return movie_info


# Entry point of the script
if __name__ == "__main__":
    # Define search criteria
    criteria = {
        "min_year": 1900,
        "max_year": 2023,
        "min_rating": 7.0,
        "max_rating": 10,
        "title_type": "movie",
        "genres": ["Action", "Drama"]
    }
    # Run the main function
    main(criteria)