import psycopg2
import random
import requests
from flask import request, redirect, url_for  # add these imports at the beginning of your file

from scripts.getGenres import get_unique_genres, conn
from tmdbsimple import Movies
import tmdbsimple as tmdb
import json
from flask import render_template, Flask

app = Flask(__name__)
tmdb.API_KEY = '1ce9398920594a5521f0d53e9b33c52f'


def get_db_connection():
    conn = psycopg2.connect(
        database="imdb_info",
        user="bryceharmon",
        password="bears2017",
        host="localhost",
        port="5432"
    )
    return conn


def execute_sql_query(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    dict_rows = [dict(zip(column_names, row)) for row in rows]
    return dict_rows


def execute_sql_query_with_random_tconst(sql_template, limit=None):
    conn = get_db_connection()
    dict_rows = []
    while not dict_rows:
        start = 1
        end = 9916880
        random_number = random.randint(start, end)
        random_number_str = str(random_number).zfill(7)
        random_tconst = 'tt' + random_number_str
        if limit is not None:
            sql_template = sql_template.replace(";", " LIMIT {} ;".format(limit))
        sql = sql_template.format(tconst=random_tconst)
        dict_rows = execute_sql_query(conn, sql)
        if dict_rows is None:
            dict_rows = []
    conn.close()
    return dict_rows


@app.route('/')
def home():
    sql_template = """
            SELECT
                tb.tconst,
                tb.titleType,
                tb.primaryTitle,
                tb.originalTitle,
                tb.isAdult,
                tb.startYear,
                tb.runtimeMinutes,
                tb.genres,
                tr.averageRating,
                tr.numVotes,
                ti.id
            FROM
            imdb_info.public.title_basics AS tb
            INNER JOIN
            imdb_info.public.title_ratings AS tr ON tb.tconst = tr.tconst
            INNER JOIN
            imdb_info.public.tmdb_info AS ti ON tb.primaryTitle = ti.original_title
            WHERE
            tb.tconst = '{tconst}' AND tb.titleType = 'movie'
            LIMIT 1;
        """

    rows = execute_sql_query_with_random_tconst(sql_template)
    movie_id = rows[0]['id']
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb.API_KEY}"
    response = requests.get(url)
    response_data = json.loads(response.text)
    poster_path = response_data['poster_path']
    print(poster_path)

    return render_template('home.html', rows=rows, poster_path=poster_path)


@app.route('/setFilters', methods=['GET', 'POST'])  # allow both GET and POST requests
def setFilters():
    conn = get_db_connection()
    genres = get_unique_genres(conn)
    if request.method == 'POST':  # this block is entered when the form is submitted
        selected_genres = request.form.getlist('mood_category2[]')  # get list of selected genres
        selected_genres = [genre.replace("_", " ").title() for genre in selected_genres]  # format genres

        # Redirect to the filteredMovies route with the selected genres as arguments
        return redirect(url_for('filtered_movies', genres=selected_genres))

    return render_template('setFilters.html', genres=genres)


@app.route('/filtered_movies')
def filtered_movies():
    # Get the genres from the URL
    selected_genres = request.args.getlist('genres')

    # Convert list to string to use in SQL query
    genres_str = ", ".join("'{}'".format(genre) for genre in selected_genres)

    conn = get_db_connection()

    # Query all movies that have any of the selected genres
    sql_template = """
            SELECT
                tb.tconst,
                tb.titleType,
                tb.primaryTitle,
                tb.originalTitle,
                tb.isAdult,
                tb.startYear,
                tb.runtimeMinutes,
                tb.genres,
                tr.averageRating,
                tr.numVotes,
                ti.id
            FROM
                imdb_info.public.title_basics AS tb
            INNER JOIN
                imdb_info.public.title_ratings AS tr ON tb.tconst = tr.tconst
            INNER JOIN
                imdb_info.public.tmdb_info AS ti ON tb.primaryTitle = ti.original_title
            WHERE
                tb.titleType = 'movie' AND 
                tb.genres && ARRAY[{}]::varchar[];
        """.format(genres_str)

    rows = execute_sql_query_with_random_tconst(sql_template, limit=1)
    conn.close()

    movie_id = rows[0]['id']
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb.API_KEY}"
    response = requests.get(url)
    response_data = json.loads(response.text)
    poster_path = response_data['poster_path']
    print(poster_path)

    return render_template('filtered_movies.html', rows=rows, poster_path=poster_path)


if __name__ == "__main__":
    app.run(debug=True)
