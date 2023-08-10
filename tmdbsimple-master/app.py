import random
import os
import pymysql
import imdb
from flask import Flask, render_template, request, redirect, url_for
from scripts.getMovieFromIMDB import get_filtered_random_row

app = Flask(__name__)

print("Current working directory:", os.getcwd())

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}


@app.route('/')
def home():
    # Get a random movie from the filtered function
    row = get_filtered_random_row(db_config, {})

    # Extract the numeric ID from the tconst
    imdbId = int(row['tconst'][2:])

    # Fetch the movie details using imdbpy
    ia = imdb.IMDb()
    movie = ia.get_movie(imdbId)

    movie_data = {
        "title": movie.get('title', 'N/A'),
        "imdb_id": movie.getID(),
        "genres": ', '.join(movie.get('genres', ['N/A'])),
        "directors": ', '.join([director['name'] for director in movie.get('director', [])]),
        "writers": ', '.join([writer['name'] for writer in movie.get('writer', []) if 'name' in writer]),
        "cast": ', '.join([actor['name'] for actor in movie.get('cast', [])][:5]),
        "runtimes": ', '.join(movie.get('runtimes', ['N/A'])),
        "countries": ', '.join(movie.get('countries', ['N/A'])),
        "languages": ', '.join(movie.get('languages', ['N/A'])),
        "rating": movie.get('rating', 'N/A'),
        "votes": movie.get('votes', 'N/A'),
        "plot": movie.get('plot', ['N/A'])[0],
        "poster_url": movie.get_fullsizeURL()
    }
    print(movie_data)

    return render_template('home.html', movie=movie_data)


@app.route('/setFilters')
def set_filters():
    return render_template('setFilters.html')


@app.route('/random_movie', methods=['POST'])
def random_movie():
    return redirect(url_for('home'))


@app.route('/filtered_movie', methods=['POST'])
def filtered_movie():
    print(request.form)
    genres = request.form.getlist('genres')

    criteria = {
        'min_year': int(request.form.get('min_year', 2000)),
        'max_year': int(request.form.get('max_year', 2020)),
        'min_rating': float(request.form.get('min_rating', 7.5)),
        'max_rating': float(request.form.get('max_rating', 10)),
        'min_votes': int(request.form.get('min_votes', 100000)),
        'title_type': request.form.get('title_type', 'movie'),
        'genres': genres
    }

    row = get_filtered_random_row(db_config, criteria)

    # Extract the numeric ID from the tconst
    imdbId = int(row['tconst'][2:])
    ia = imdb.IMDb()
    movie = ia.get_movie(imdbId)

    movie_data = {
        "title": movie.get('title', 'N/A'),
        "imdb_id": movie.getID(),
        "genres": ', '.join(movie.get('genres', ['N/A'])),
        "directors": ', '.join([director['name'] for director in movie.get('director', [])]),
        "writers": ', '.join([writer['name'] for writer in movie.get('writer', []) if 'name' in writer]),
        "cast": ', '.join([actor['name'] for actor in movie.get('cast', [])][:5]),
        "runtimes": ', '.join(movie.get('runtimes', ['N/A'])),
        "countries": ', '.join(movie.get('countries', ['N/A'])),
        "languages": ', '.join(movie.get('languages', ['N/A'])),
        "rating": movie.get('rating', 'N/A'),
        "votes": movie.get('votes', 'N/A'),
        "plot": movie.get('plot', ['N/A'])[0],
        "poster_url": movie.get_fullsizeURL()
    }

    return render_template('filtered_movies.html', movie=movie_data)


if __name__ == "__main__":
    app.run(debug=True)
