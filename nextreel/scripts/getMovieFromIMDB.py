import random
import pymysql
import imdb
import random
import pymysql
import imdb

#
#
#
#
#
#
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'caching_sha2_password',
#     'database': 'imdb'
# }
#
# def get_db_connection(db_config):
#     """Establish a connection to the database."""
#     return pymysql.connect(
#         host=db_config['host'],
#         user=db_config['user'],
#         password=db_config['password'],
#         database=db_config['database']
#     )
#
#
#
#
# def get_random_row_value(db_config, table_name, column_name):
#     """Fetch a random row value based on column name."""
#     with get_db_connection(db_config) as connection:
#         with connection.cursor() as cursor:
#             cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
#             total_rows = cursor.fetchone()[0]
#
#             random_row_num = random.randint(1, total_rows)
#             cursor.execute(f"SELECT {column_name} FROM `{table_name}` LIMIT {random_row_num - 1}, 1")
#             random_value = cursor.fetchone()[0]
#
#             cursor.execute("SELECT * FROM `{}` WHERE {} = %s".format(table_name, column_name), (random_value,))
#             random_row = cursor.fetchone()
#             column_names = [desc[0] for desc in cursor.description]
#
#         return dict(zip(column_names, random_row))
#
#
# def get_filtered_random_row(db_config, criteria):
#     """Fetch a random row based on filter criteria."""
#     min_year = criteria.get('min_year', 2000)
#     max_year = criteria.get('max_year', 2020)
#     min_rating = criteria.get('min_rating', 7.5)
#     max_rating = criteria.get('max_rating', 10)
#     min_votes = criteria.get('min_votes', 100000)
#     title_type = criteria.get('title_type', 'movie')
#     genres = criteria.get('genres')
#
#     parameters = [min_year, max_year, min_rating, max_rating, min_votes, title_type]
#
#     with get_db_connection(db_config) as connection:
#         with connection.cursor() as cursor:
#             # Base query
#             query = """
#             SELECT tb.*
#             FROM `title.basics` tb
#             JOIN `title.ratings` tr ON tb.tconst = tr.tconst
#             WHERE tb.startYear >= %s AND tb.startYear <= %s
#             AND tr.averagerating >= %s AND tr.averagerating <= %s
#             AND tr.numVotes >= %s
#             AND tb.titleType = %s
#             """
#
#             # Add genres filter if provided
#             if genres:
#                 genre_conditions = ["tb.genres LIKE %s" for _ in genres]
#                 query += " AND (" + " OR ".join(genre_conditions) + ")"
#                 parameters.extend(["%" + genre + "%" for genre in genres])
#
#             query += " ORDER BY RAND() LIMIT 1"
#
#             print("Generated SQL Query:", query)
#             print("Query Parameters:", parameters)
#
#             cursor.execute(query, parameters)
#             random_row = cursor.fetchone()
#
#             if not random_row:
#                 return None
#
#             column_names = [desc[0] for desc in cursor.description]
#         return dict(zip(column_names, random_row))
#
#
# def fetch_movie_info_from_imdb(tconst):
#     """Fetch movie information from IMDb using IMDbPY."""
#     imdbId = int(tconst[2:])
#     ia = imdb.IMDb()
#     return ia.get_movie(imdbId)
#
#
# def main(criteria):
#     """Main function to test fetching random movies based on criteria."""
#     row = get_filtered_random_row(db_config, criteria)
#     if not row:
#         print("No movies found based on the given criteria.")
#         return None
#
#     movie_info = fetch_movie_info_from_imdb(row['tconst'])
#     return movie_info
#
#     # Print the movie details
#     print("Movie Title:", movie_info['title'])
#     print("Year:", movie_info['year'])
#     print("Rating:", movie_info['rating'])
#     print("Genres:", ", ".join(movie_info['genres']))
#     print("Plot:", movie_info.get('plot outline', 'No plot outline available.'))
#     print("Cast:", ", ".join([str(actor) for actor in movie_info['cast'][:5]]))  # Displaying top 5 actors
#     print("Runtime(s):", ', '.join(movie_info.get('runtimes', ['N/A'])))
#     print("Country(s):", ', '.join(movie_info.get('countries', ['N/A'])))
#     print("Language(s):", ', '.join(movie_info.get('languages', ['N/A'])))
#     print("Rating:", movie_info.get('rating', 'N/A'))
#     print("Number of Votes:", movie_info.get('votes', 'N/A'))
#     print("Plot:", movie_info.get('plot', ['N/A'])[0])
#
#     # You can add more fields as needed.
#     print("=" * 50)
#
#     # Add any other movie details you'd like to display here.
#
#
# if __name__ == "__main__":
#     criteria = {
#         "min_year": 2000,
#         "max_year": 2020,
#         "min_rating": 7.5,
#         "max_rating": 10,
#         "title_type": "movie",
#         "genres": ["Action", "Drama"]
#     }
#     main(criteria)
#
#
# # import random
# # import pymysql
# # import imdb
# # from mysql_query_builder import execute_query  # Import the query builder function
# #
# # db_config = {
# #     'host': 'localhost',
# #     'user': 'root',
# #     'password': 'caching_sha2_password',
# #     'database': 'imdb'
# # }
# #
# #
# # def get_db_connection(db_config):
# #     """Establish a connection to the database."""
# #     return pymysql.connect(
# #         host=db_config['host'],
# #         user=db_config['user'],
# #         password=db_config['password'],
# #         database=db_config['database']
# #     )
# #
# #
# # def get_random_row_value(db_config, table_name, column_name):
# #     """Fetch a random row value based on column name."""
# #
# #     # Count the total number of rows in the table
# #     count_query = f"SELECT COUNT(*) FROM `{table_name}`"
# #     total_rows = execute_query(db_config, count_query)[0][0]
# #
# #     # Generate a random row number
# #     random_row_num = random.randint(1, total_rows)
# #
# #     # Fetch the value of the specific column at the random row
# #     value_query = f"SELECT {column_name} FROM `{table_name}` LIMIT %s, 1"
# #     random_value = execute_query(db_config, value_query, (random_row_num - 1,))[0][0]
# #
# #     # Fetch all column values for the row where column_name equals random_value
# #     row_query = f"SELECT * FROM `{table_name}` WHERE {column_name} = %s"
# #     random_row = execute_query(db_config, row_query, (random_value,))[0]
# #     column_names = [desc[0] for desc in random_row]
# #
# #     return dict(zip(column_names, random_row))
# #
# #
# # def get_filtered_random_row(db_config, criteria):
# #     min_year = criteria.get('min_year', 2000)
# #     max_year = criteria.get('max_year', 2020)
# #     min_rating = criteria.get('min_rating', 7.5)
# #     max_rating = criteria.get('max_rating', 10)
# #     min_votes = criteria.get('min_votes', 100000)
# #     title_type = criteria.get('title_type', 'movie')
# #     genres = criteria.get('genres')
# #
# #     parameters = [min_year, max_year, min_rating, max_rating, min_votes, title_type]
# #
# #     genre_conditions = ["tb.genres LIKE %s" for _ in genres] if genres else []
# #
# #     query = """
# #     SELECT tb.*
# #     FROM `title.basics` tb
# #     JOIN `title.ratings` tr ON tb.tconst = tr.tconst
# #     WHERE tb.startYear >= %s AND tb.startYear <= %s
# #     AND tr.averagerating >= %s AND tr.averagerating <= %s
# #     AND tr.numVotes >= %s
# #     AND tb.titleType = %s
# #     """ + (" AND (" + " OR ".join(genre_conditions) + ")" if genres else "") + " ORDER BY RAND() LIMIT 1"
# #
# #     if genres:
# #         parameters.extend(["%" + genre + "%" for genre in genres])
# #
# #     random_row = execute_query(db_config, query, parameters)
# #     return random_row
# #
# #
# # def fetch_movie_info_from_imdb(tconst):
# #     imdbId = int(tconst[2:])
# #     ia = imdb.IMDb()
# #     return ia.get_movie(imdbId)
# #
# #
# # def main(criteria):
# #     row = get_filtered_random_row(db_config, criteria)
# #     if not row:
# #         print("No movies found based on the given criteria.")
# #         return None
# #
# #     movie_info = fetch_movie_info_from_imdb(row['tconst'])
# #     return movie_info
# #
# #
# # if __name__ == "__main__":
# #     criteria = {
# #         "min_year": 2000,
# #         "max_year": 2020,
# #         "min_rating": 7.5,
# #         "max_rating": 10,
# #         "title_type": "movie",
# #         "genres": ["Action", "Drama"]
# #     }
# #     main(criteria)
# #
# #


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

    movie_info = fetch_movie_info_from_imdb(row['tconst'])
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
