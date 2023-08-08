import random

import imdb
import pymysql
from flask import render_template, Flask
from scripts.getMovieFromIMDB import get_movie_tconst
from scripts.setFilters import get_random_row_value
from scripts.setFilters import get_filtered_random_row
from scripts.setFilters import get_random_row_value, get_rating_by_tconst, get_filtered_random_row

import os


app = Flask(__name__)

print("Current working directory:", os.getcwd())

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}


def get_random_movie(db_config):
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:  # Use DictCursor
            # Find the total number of movie rows in the table
            cursor.execute("SELECT COUNT(*) FROM `title.basics` WHERE titleType = 'movie'")
            total_rows = cursor.fetchone()['COUNT(*)']

            # Select a random row number
            random_row_num = random.randint(1, total_rows)

            # Fetch a random movie row
            cursor.execute("SELECT * FROM `title.basics` WHERE titleType = 'movie' LIMIT %s, 1", (random_row_num - 1,))
            random_movie = cursor.fetchone()

        return random_movie
    finally:
        connection.close()


def get_rating_by_tconst(db_config, tconst):
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

    try:
        with connection.cursor() as cursor:
            # Fetch the rating information based on the tconst
            cursor.execute("SELECT * FROM `title.ratings` WHERE tconst = %s", (tconst,))
            rating_info = cursor.fetchone()

        return rating_info
    finally:
        connection.close()


@app.route('/')
def home():
    # Get tconst for the movie
    tconst = get_movie_tconst()

    # Extract the numeric ID from the tconst
    imdbId = int(tconst[2:])

    # Fetch the movie details using imdbpy
    ia = imdb.IMDb()
    movie = ia.get_movie(imdbId)

    movie_data = {
        "title": movie.get('title', 'N/A'),
        "imdb_id": movie.getID(),
        "genres": ', '.join(movie.get('genres', ['N/A'])),
        "directors": ', '.join([director['name'] for director in movie.get('director', [])]),
        "writers": ', '.join([writer['name'] for writer in movie.get('writer', []) if 'name' in writer]),
        "cast": ', '.join([actor['name'] for actor in movie.get('cast', [])]),
        "runtimes": ', '.join(movie.get('runtimes', ['N/A'])),
        "countries": ', '.join(movie.get('countries', ['N/A'])),
        "languages": ', '.join(movie.get('languages', ['N/A'])),
        "rating": movie.get('rating', 'N/A'),
        "votes": movie.get('votes', 'N/A'),
        "plot": movie.get('plot', ['N/A'])[0]
    }
    print(movie_data)

    return render_template('home.html', movie=movie_data)


if __name__ == "__main__":
    app.run(debug=True)