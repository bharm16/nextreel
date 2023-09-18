import random
import time

import pymysql
import imdb
import random
import pymysql
import imdb

import sys

from nextreel.scripts.mysql_query_builder import execute_query

# print("Python Executable:", sys.executable)

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


def get_filtered_random_row(db_config, criteria):
    min_year = criteria.get('min_year', 1900)
    max_year = criteria.get('max_year', 2023)
    min_rating = criteria.get('min_rating', 7.0)
    max_rating = criteria.get('max_rating', 10)
    min_votes = criteria.get('min_votes', 100000)
    title_type = criteria.get('title_type', 'movie')
    genres = criteria.get('genres')
    language = criteria.get('language', 'en')  # Add this line

    parameters = [min_year, max_year, min_rating, max_rating, min_votes, title_type, language]  # Add language here

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
    AND ta.language = %s  -- Add this line
    """ + (" AND (" + " OR ".join(genre_conditions) + ")" if genres else "") + " ORDER BY RAND() LIMIT 1"

    if genres:
        parameters.extend(["%" + genre + "%" for genre in genres])

    print("GFRR Generated SQL Query:", query)
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





from concurrent.futures import ThreadPoolExecutor


def fetch_movie_data(movie, movies_data):
    """Fetch movie details from IMDb and append to movies_data list."""
    movie_info = fetch_movie_info_from_imdb(movie['tconst'])
    movie_data = {
        "title": movie_info.get('title', 'N/A'),
        "imdb_id": movie_info.getID(),
        "genres": ', '.join(movie_info.get('genres', ['N/A'])),
        "directors": ', '.join([director['name'] for director in movie_info.get('director', [])][:1]),
        "writer": movie_info.get('writer', [])[0]['name'] if movie_info.get('writer') else None,
        "cast": ', '.join([actor['name'] for actor in movie_info.get('cast', [])][:3]),
        "runtimes": ', '.join(movie_info.get('runtimes', ['N/A'])),
        "countries": ', '.join(movie_info.get('countries', ['N/A'])),
        "languages": ', '.join(movie_info.get('languages', ['N/A'])),
        "rating": movie_info.get('rating', 'N/A'),
        "votes": movie_info.get('votes', 'N/A'),
        "plot": movie_info.get('plot', ['N/A'])[0],
        "poster_url": movie_info.get_fullsizeURL(),
    }
    movies_data.append(movie_data)


from concurrent.futures import ThreadPoolExecutor

def get_all_movies_by_actor(db_config, nconst):
    query = """
    SELECT tb.*
    FROM `title.basics` tb
    JOIN `title.principals` tp ON tb.tconst = tp.tconst
    WHERE tp.nconst = %s 
    AND tb.titleType = 'movie'
    AND tp.category = 'actor'
    """
    parameters = [nconst]
    print("Generated SQL Query for get_all_movies_by_actor:", query)
    print("Query Parameters:", parameters)
    all_movies = execute_query(db_config, query, parameters, fetch='all')
    movies_data = []

    if all_movies:
        # Increase max_workers to a higher value depending on your system's capability
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(fetch_movie_data, all_movies, [movies_data] * len(all_movies))

    return movies_data if movies_data else None




def main(criteria):
    """Main function to execute the program."""
    # Fetch a random movie row that matches the criteria
    row = get_filtered_random_row(db_config, criteria)
    if not row:
        print("No movies found based on the given criteria.")
        return None

    # Record the start time for fetching movie info
    # start_time = time.time()

    # Fetch movie info from IMDb
    movie_info = fetch_movie_info_from_imdb(row['tconst'])

    # Record the end time for fetching movie info
    # end_time = time.time()

    print("Fetched movie genres:", movie_info.get('genres'))

    # Calculate and print the time taken to fetch movie info
    # elapsed_time = end_time - start_time
    # print(f"Time taken by fetch_movie_info_from_imdb: {elapsed_time} seconds")

    # Fetch all movies by a specific actor
    nconst = "nm0000093"  # Replace this with the actor's IMDb ID (nconst)
    actor_movies = get_all_movies_by_actor(db_config, nconst)
    print(f"Debug actor_movies: {actor_movies}")
    if actor_movies:
        print(f"Movies by actor {nconst}:")
        for movie in actor_movies:
            print(movie['tconst'], movie['primaryTitle'])
    else:
        print(f"No movies found for actor {nconst}.")

    return movie_info





def get_nconst_from_actor_name(db_config, actor_name):
    """Fetch the nconst (IMDb identifier) for an actor based on their name."""
    # SQL query to fetch the nconst by actor_name from the `name.basics` table
    query = """
    SELECT nconst FROM `name.basics`
    WHERE primaryName = %s
    LIMIT 1
    """

    # Query parameters
    parameters = [actor_name]

    # Debug output for the generated SQL query and parameters
    print("Generated SQL Query for get_nconst_from_actor_name:", query)
    print("Query Parameters:", parameters)

    # Execute the query
    result = execute_query(db_config, query, parameters, fetch='one')

    if result:
        return result['nconst']
    else:
        return None



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
