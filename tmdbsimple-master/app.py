import random
import pymysql
import requests
from flask import request, redirect, url_for
import tmdbsimple as tmdb
import json
from flask import render_template, Flask
from flask import render_template
from scripts.randomIMDBGenerator import get_random_row_value, get_rating_by_tconst

app = Flask(__name__)

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
        with connection.cursor() as cursor:
            # Find the total number of movie rows in the table
            cursor.execute("SELECT COUNT(*) FROM `title.basics` WHERE titleType = 'movie'")
            total_rows = cursor.fetchone()[0]

            # Select a random row number
            random_row_num = random.randint(1, total_rows)

            # Fetch a random movie row
            cursor.execute("SELECT * FROM `title.basics` WHERE titleType = 'movie' LIMIT %s, 1", (random_row_num - 1,))
            random_movie = cursor.fetchone()

        return random_movie
    finally:
        connection.close()


print(get_random_movie(db_config))


def get_db_connection():
    conn = pymysql.connect(
        database="imdb",
        user="root",
        password="caching_sha2_password",
        host="localhost",
        port=3306
    )
    return conn


@app.route('/')
def home():
    # Fetch data from randomIMDBgenerator
    random_row = get_random_row_value(db_config, 'title.basics', 'tconst')
    rating_info = get_rating_by_tconst(db_config, random_row['tconst'])

    # Merge the data
    row_data = {**random_row, **{
        'averagerating': rating_info[1],
        'numvotes': rating_info[2]
    }}

    return render_template('home.html', row=row_data, poster_path="your_tmdb_poster_path")


if __name__ == "__main__":
    app.run(debug=True)
