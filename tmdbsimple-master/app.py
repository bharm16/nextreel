import random
import os
import pymysql
import imdb
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from scripts.getMovieFromIMDB import get_filtered_random_row, main
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask import jsonify
from scripts.logMovieToAccount import log_movie_to_account

app = Flask(__name__)
app.secret_key = 'some_random_secret_key'  # Make sure to change this in production

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

should_logout_on_home_load = True


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


# User loader function
# User loader function
@login_manager.user_loader
def load_user(user_id):
    conn = pymysql.connect(**user_db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    if user_data:
        return User(id=user_data['id'], username=user_data['username'])
    return None


print("Current working directory:", os.getcwd())

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}

# Configuration for User Accounts database
user_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'UserAccounts'
}


@app.route('/')
def home():
    global should_logout_on_home_load
    if should_logout_on_home_load:
        logout_user()
        should_logout_on_home_load = False

    row = get_filtered_random_row(db_config, {})
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
    print(movie_data)
    return render_template('home.html', movie=movie_data, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Entered login function")  # Debugging line
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Attempting to authenticate {username}")  # Debugging line

        conn = pymysql.connect(**user_db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        print(f"User data fetched: {user_data}")  # Debugging line

        if user_data and user_data['password'] == password:
            print("Successfully authenticated!")  # Debugging line
            user = User(id=user_data['id'], username=user_data['username'])
            login_user(user)
            return redirect(url_for('home'))
        else:
            print("Failed to authenticate!")  # Debugging line
            flash("Invalid username or password")
    return render_template('userLogin.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         conn = pymysql.connect(**user_db_config)
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
#         user_data = cursor.fetchone()
#         cursor.close()
#         conn.close()
#
#         if user_data and check_password_hash(user_data['password'], password):
#             print(f"Test output: Username and password match found for user {username}")  # Test output
#             user = User(id=user_data['id'], username=user_data['username'])
#             login_user(user)
#             return redirect(url_for('home'))
#         else:
#             flash("Invalid username or password")
#     return render_template('userLogin.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = pymysql.connect(**user_db_config)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Registration successful! Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/setFilters')
def set_filters():
    return render_template('setFilters.html')


@app.route('/random_movie', methods=['POST'])
def random_movie():
    return redirect(url_for('home'))


@app.route('/filtered_movie', methods=['POST'])
def filtered_movie_endpoint():
    filters = request.form
    criteria = {
        "min_year": 2000,
        "max_year": 2020,
        "min_rating": 7.5,
        "max_rating": 10,
        "title_type": "movie"
    }
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

    return render_template('filtered_movies.html', movie=movie_data)


@app.route('/seen_it', methods=['POST'])
@login_required
def seen_it():
    tconst = request.json.get('tconst')
    if tconst:
        log_movie_to_account(current_user.id, tconst, user_db_config)  # Log the movie to watched_movies table
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failure', 'message': 'No tconst provided'}), 400


if __name__ == "__main__":
    app.run(debug=True)
