import random
import os
import pymysql
import imdb
from flask import Flask, render_template, request, redirect, url_for
from scripts.getMovieFromIMDB import get_filtered_random_row, main
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


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
@app.route('/filtered_movie', methods=['POST'])
def filtered_movie_endpoint():
    filters = request.form

    # Create a criteria dictionary with default values
    criteria = {
        "min_year": 2000,
        "max_year": 2020,
        "min_rating": 7.5,
        "max_rating": 10,
        "title_type": "movie"
    }

    # Update criteria based on filters received
    if filters.get('year_min'):
        criteria['min_year'] = int(filters.get('year_min'))

    if filters.get('year_max'):
        criteria['max_year'] = int(filters.get('year_max'))

    if filters.get('imdb_score_min'):
        criteria['min_rating'] = float(filters.get('imdb_score_min'))

    if filters.get('imdb_score_max'):
        criteria['max_rating'] = float(filters.get('imdb_score_max'))

    if filters.get('num_votes_min'):
        criteria['min_votes'] = int(filters.get('num_votes_min'))

    movie_info = main(criteria)

    if not movie_info:
        # Handle cases where no movie is found based on criteria.
        return "No movies found based on the given criteria."

    movie_data = {
        "title": movie_info.get('title', 'N/A'),
        "imdb_id": movie_info.getID(),
        "genres": ', '.join(movie_info.get('genres', ['N/A'])),
        "directors": ', '.join([director['name'] for director in movie_info.get('director', [])]),
        "writers": ', '.join([writer['name'] for writer in movie_info.get('writer', []) if 'name' in writer]),
        "cast": ', '.join([actor['name'] for actor in movie_info.get('cast', [])][:5]),
        "runtimes": ', '.join(movie_info.get('runtimes', ['N/A'])),
        "countries": ', '.join(movie_info.get('countries', ['N/A'])),
        "languages": ', '.join(movie_info.get('languages', ['N/A'])),
        "rating": movie_info.get('rating', 'N/A'),
        "votes": movie_info.get('votes', 'N/A'),
        "plot": movie_info.get('plot', ['N/A'])[0],
        "poster_url": movie_info.get_fullsizeURL()
    }
    print(movie_data)

    return render_template('filtered_movies.html',movie=movie_data)
    # You can also have a different template for filtered movies if you want.



    # # This will just return a success message for now. Adjust as necessary.
    # return "Filtered movie info printed."




if __name__ == "__main__":
    app.run(debug=True)
