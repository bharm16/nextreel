# Import required libraries
import random
import os
import time
import pymysql
import imdb
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from nextreel.scripts.account import Account

from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

from nextreel.scripts.db_config_scripts import db_config, user_db_config
from nextreel.scripts.get_user_account import get_watched_movie_posters, get_watched_movies, get_watched_movie_details, \
    get_all_movies_in_watchlist, get_all_watched_movie_details_by_user, get_all_movies_in_watchlist, insert_new_user, \
    get_user_login, get_user_by_id
from nextreel.scripts.log_movie_to_account import log_movie_to_account, update_title_basics_if_empty, \
    add_movie_to_watchlist
from nextreel.scripts.movie import Movie
from nextreel.scripts.person import Person
from nextreel.scripts.set_filters_for_nextreel_backend import ImdbRandomMovieFetcher, extract_movie_filter_criteria
from queue import Queue, Empty
import threading

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'some_random_secret_key'  # IMPORTANT: Change this in production

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Variable to determine whether a user should be logged out when the home page loads
should_logout_on_home_load = True

# Initialize a global queue to hold movie data
movie_queue = Queue(maxsize=3)

from nextreel.scripts.get_user_account import get_watched_movie_posters, get_watched_movies, get_watched_movie_details, \
    get_all_movies_in_watchlist, get_all_watched_movie_details_by_user, get_all_movies_in_watchlist

# Assuming ImdbRandomMovieFetcher is imported or defined above


import time


def populate_movie_queue():
    # Initialize sets to store watched movies and watchlist movies if the user is logged in
    watched_movies = set()
    watchlist_movies = set()

    # Create an instance of ImdbRandomMovieFetcher
    movie_fetcher = ImdbRandomMovieFetcher(db_config)

    while True:
        # Check if current_user is not None and if the user is authenticated
        if current_user and current_user.is_authenticated:
            # Update the watched_movies and watchlist_movies sets from the DB
            watched_movies = set([movie['tconst'] for movie in get_all_watched_movie_details_by_user(current_user.id)])
            watchlist_movies = set([movie['tconst'] for movie in get_all_movies_in_watchlist(current_user.id)])

        # If the queue size is less than 2, fetch a new movie
        if movie_queue.qsize() < 2:
            # Use the fetch_random_movie method from ImdbRandomMovieFetcher
            row = movie_fetcher.fetch_random_movie({})
            # row = movie_fetcher.fetch_random_movie({'language': 'en'})
            tconst = row['tconst'] if row else None

            # Ensure that the movie is neither in the watched list nor in the watchlist
            if tconst and (tconst not in watched_movies) and (tconst not in watchlist_movies):
                # Create a Movie instance and fetch the movie data
                movie = Movie(tconst, db_config)

                # Fetch and generate detailed movie information
                movie_data = movie.get_movie_data()

                # Put the fetched movie into the global queue
                movie_queue.put(movie_data)

                # Update the title_basics table if any data is missing
                # Assuming update_title_basics_if_empty() is defined elsewhere in your code
                update_title_basics_if_empty(tconst, movie_data['plot'], movie_data['poster_url'],
                                             movie_data['languages'], db_config)

            # Pause for 1 second to prevent rapid API calls
            time.sleep(1)


# Don't forget to import other required modules and functions


# Start a thread to populate the movie queue
# Start a background thread to populate the movie queue
populate_thread = threading.Thread(target=populate_movie_queue)
populate_thread.daemon = True  # Set the thread as a daemon
populate_thread.start()


@app.route('/account_settings')
@login_required
def account_settings():
    print("Current user's email:", current_user.email)

    # Render the account settings template
    return render_template('user_account_settings.html')


@app.route('/watched_movies')
@login_required
def watched_movies():
    # Initialize Account object with current user's details
    current_account = Account(id=current_user.id, username=current_user.username, email=current_user.email)

    # Fetch all watched movie details for the current user
    watched_movie_details = current_account.get_watched_movies_by_user(current_account.id)

    # Sort the list by tconst
    if watched_movie_details:  # Check if the list is not None or empty
        watched_movie_details.sort(key=lambda x: x['tconst'])

    if watched_movie_details is None:
        flash("No watched movies found for this user.")

    return render_template('watched_movies.html', watched_movie_details=watched_movie_details)


@login_manager.user_loader
def load_user(user_id):
    # Query to fetch user details from the database
    # user_data = execute_query(user_db_config, "SELECT * FROM users WHERE id=%s", (user_id,))
    user_data = get_user_by_id(user_id)
    # If user data exists, return a User object
    if user_data:
        return Account(id=user_data['id'], username=user_data['username'], email=user_data['email'])  # Add email here
    # Otherwise, return None


# Declare a global variable to store the last displayed movie
global last_displayed_movie


@app.route('/')
def home():
    global should_logout_on_home_load
    # Logout the user if the flag is set
    if should_logout_on_home_load:
        logout_user()
        should_logout_on_home_load = False

    # Fetch a movie from the global queue
    # (consider adding additional logic here to ensure the movie is appropriate for the user)
    movie_data = movie_queue.get()

    # Update the global variable with the fetched movie data
    global last_displayed_movie
    last_displayed_movie = movie_data

    # Render the home page with the fetched movie data
    return render_template('home.html', movie=movie_data, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Call the class method, passing in db_config explicitly
        user_data = Account.login_user(username, password, user_db_config)

        if user_data:
            # Create an Account instance for this user
            user = Account(id=user_data['id'], username=user_data['username'], email=user_data['email'])
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password")

    return render_template('user_login.html')


# Route for logout
@app.route('/logout')
@login_required  # Require the user to be logged in to access this route
def logout():
    # Log the user out
    logout_user()
    # Redirect to the login page
    return redirect(url_for('login'))


# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        result = Account.register_user(username, email, password)

        if result == "Username already exists.":
            flash("Username already exists.")
            return render_template('create_account_form.html')

        flash("ShowModal")
        return redirect(url_for('login'))

    return render_template('create_account_form.html')


# Route for setting filters
@app.route('/setFilters')
def set_filters():
    # Render the filter settings template
    return render_template('set_filters.html')


@app.route('/filtered_movie', methods=['POST'])
def filtered_movie_endpoint():
    # Extract filter criteria from the form using the extract_movie_filter_criteria function
    criteria = extract_movie_filter_criteria(request.form)

    print("Extracted criteria:", criteria)

    movie_fetcher = ImdbRandomMovieFetcher(db_config)

    # Fetch a random movie row that matches the criteria using the fetch_random_movie method
    row = movie_fetcher.fetch_random_movie(criteria)

    # If no movies are found, return an error message
    if not row:
        return "No movies found based on the given criteria."

    # Create a Movie instance and fetch the movie data
    movie = Movie(row['tconst'], db_config)

    # Fetch and generate detailed movie information using the get_movie_data method
    movie_data = movie.get_movie_data()

    # Render the template with the filtered movie
    return render_template('filtered_movies.html', movie=movie_data)


# Route to load the next movie from the queue
@app.route('/next_movie', methods=['GET', 'POST'])
def next_movie():
    global last_displayed_movie  # Use the global variable to get the last displayed movie

    # If there is a last displayed movie, just replace it with the next one from the queue
    if last_displayed_movie:
        # Get the next movie from the queue
        next_movie_data = movie_queue.get()

        # Update the global variable with the new movie data
        last_displayed_movie = next_movie_data

        # Redirect to the home page
        return redirect(url_for('home'))
    else:
        # Return an error if no movies are in the queue
        return jsonify({'status': 'failure', 'message': 'No movies in the queue'}), 400


# Assuming current_user is an instance of Account
@app.route('/seen_it', methods=['POST'])
@login_required
def seen_it():
    global last_displayed_movie
    if last_displayed_movie:
        tconst = last_displayed_movie.get("imdb_id")
        current_user.log_movie_to_user_account(current_user.id, current_user.username, tconst, last_displayed_movie,
                                               user_db_config)
        return redirect(url_for('home'))
    else:
        return jsonify({'status': 'failure', 'message': 'No movies in the queue'}), 400


@app.route('/actor/<actor_name>', methods=['GET'])
def get_movies_by_actor(actor_name):
    start_time = time.time()  # Record the start time

    # Create a Person object
    actor = Person(db_config, actor_name)

    # Use the Person object to fetch actor's details
    fetched_actor = actor.actor_info

    if fetched_actor is None:
        return "Actor not found", 404

    # Convert the actor information to a dictionary
    actor_dict = fetched_actor.data

    # Fetch the actor's filmography (this assumes that 'filmography' is a key in actor_dict)
    actor_filmography = actor_dict.get('filmography', {})

    end_time = time.time()  # Record the end time
    print(f"Time taken for database queries: {end_time - start_time} seconds")

    # Render a template to display the actor's details and filmography
    return render_template('actor_movies.html', actor_dict=actor_dict, actor_filmography=actor_filmography,
                           actor_name=actor_name)


@app.route('/add_to_watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    global last_displayed_movie  # Consider using a different state management approach
    if last_displayed_movie:
        tconst = last_displayed_movie.get("imdb_id")

        # Assuming current_user is an instance of Account
        current_user.add_movie_to_watchlist(current_user.id, current_user.username, tconst, last_displayed_movie,
                                            user_db_config)

        return redirect(url_for('home'))
    else:
        return jsonify({'status': 'failure', 'message': 'No movies in the queue'}), 400


@app.route('/user_watch_list')
@login_required
def user_watch_list():
    watchlist_movies = get_all_movies_in_watchlist(current_user.id)
    return render_template('user_watchlist.html', watchlist_movies=watchlist_movies)


if __name__ == "__main__":
    # Run the Flask app in debug mode (change this in production)
    app.run(debug=True)
