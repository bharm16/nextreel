# Import required libraries
import time
from queue import Queue

import tmdb
from flask import Flask, redirect, url_for, jsonify
from flask_login import login_required, user_logged_in
from flask_mailman import Mail
from flask_security import hash_password

from nextreel import flask_security
from nextreel.flask_security import db, setup_security
from nextreel.scripts.account import Account
from nextreel.scripts.db_config_scripts import db_config, user_db_config
from nextreel.scripts.get_user_account import get_all_movies_in_watchlist
from nextreel.scripts.movie_queue import MovieQueue
from nextreel.scripts.set_filters_for_nextreel_backend import ImdbRandomMovieFetcher, extract_movie_filter_criteria
from nextreel.scripts.tmdb_data import get_backdrop_image_for_home

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'some_random_secret_key'  # IMPORTANT: Change this in production

default_movie_tmdb_id = 62  # This is the TMDb ID for the movie "Fight Club"
default_backdrop_url = get_backdrop_image_for_home(default_movie_tmdb_id)

# Your existing database configuration
user_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'UserAccounts'
}

# Convert database configuration to SQLAlchemy database URI
db_uri = f"mysql://{user_db_config['user']}:{user_db_config['password']}@{user_db_config['host']}/{user_db_config['database']}"

# Configure your app to use MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some_random_secret_key'
app.config['SECURITY_PASSWORD_SALT'] = 'some_random_salt'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True

# Assuming you've already configured your app with MAIL settings
# Example configuration (you'd replace these with your actual settings):
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'username'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@example.com'  # Optional: Default sender

# Configure a mock email server
app.config['MAIL_BACKEND'] = 'console'  # Use the console backend
app.config['MAIL_SUPPRESS_SEND'] = True  # Suppress sending emails for testing

# Step 4: Initialize the Mail object
mail = Mail(app)


# Initialize SQLAlchemy
db.init_app(app)

# # Setup Flask-Security
# setup_security(app)
user_datastore = setup_security(app)


# Function to create a user and role
def create_user():
    with app.app_context():
        # Create a user to test with
        user_datastore.create_user(email="test@me.com", password=hash_password("password"))
        db.session.commit()

        # Create and assign the admin role to the admin user
        admin_role = user_datastore.find_or_create_role(name="admin", description="Administrator")
        admin_user = user_datastore.get_user("test@me.com")
        user_datastore.add_role_to_user(admin_user, admin_role)
        db.session.commit()


# Set it as a global template variable
@app.context_processor
def inject_default_backdrop_url():
    return dict(default_backdrop_url=default_backdrop_url)


# # Initialize Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)

# Variable to determine whether a user should be logged out when the home page loads
should_logout_on_home_load = True

# Define global variables to hold the movie fetcher and criteria
global_movie_fetcher = ImdbRandomMovieFetcher(db_config)
global_criteria = {}  # Start with empty criteria; can be updated dynamically

# Set your TMDb API key
tmdb.API_KEY = '1ce9398920594a5521f0d53e9b33c52f'

# Initialize movie queue and its manager
movie_queue = Queue(maxsize=25)
movie_queue_manager = MovieQueue(db_config, movie_queue)

# Optionally check that the thread is alive
print("Is populate_thread alive?", movie_queue_manager.is_thread_alive())

# Initialize two lists to act as stacks for previous and future movies

future_movies_stack = []
previous_movies_stack = []
current_displayed_movie = None


def fetch_and_render_movie(movie_queue, current_displayed_movie, previous_movies_stack, criteria=None):
    """Fetch a movie from the given queue and render the movie template."""
    # Check if the queue is empty
    if movie_queue.empty():
        print("The movie queue is empty.")
        return "The movie queue is empty.", 404

    # Fetch the next movie from the queue
    current_movie_data = movie_queue.get()

    # Update the global current_displayed_movie
    current_displayed_movie = current_movie_data

    # Append the current displayed movie to the previous_movies_stack
    previous_movies_stack.append(current_movie_data)

    # Render the movie template, also passing the length of previous_movies_stack for UI control
    return render_template('movie.html',
                           movie=current_movie_data,
                           current_user=current_user,
                           previous_count=len(previous_movies_stack))


@app.route('/movie')
def movie():
    global movie_queue, current_displayed_movie, previous_movies_stack  # Declare global variables
    return fetch_and_render_movie(movie_queue, current_displayed_movie, previous_movies_stack)


@app.route('/filtered_movie', methods=['POST'])
def filtered_movie_endpoint():
    global movie_queue, current_displayed_movie, previous_movies_stack  # Declare global variables
    global global_movie_fetcher, global_criteria  # Additional global variables

    # Extract new filter criteria from the form
    new_criteria = extract_movie_filter_criteria(request.form)

    # Update global criteria
    global_criteria = new_criteria

    # Initialize a new movie queue and its manager with the updated filter criteria
    movie_queue_manager = MovieQueue(db_config, movie_queue, global_criteria)

    # Debugging
    print("Extracted criteria:", new_criteria)
    movie_queue_manager.is_thread_alive()

    # Wait for a few seconds to give the thread some time to populate the queue
    time.sleep(5)

    return fetch_and_render_movie(movie_queue, current_displayed_movie, previous_movies_stack, criteria=new_criteria)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/account_settings')
@login_required
def account_settings():
    print("Current user's email:", current_user.email)

    # Render the account settings template
    return render_template('user_account_settings.html')


from flask import request, render_template, flash
from flask_login import login_required, current_user
from nextreel.scripts.sort_and_filter import sort_movies, get_filtered_watched_movies  # Import the sorting function


@app.route('/watched_movies')
@login_required
def watched_movies():
    # Initialize Account object with current user's details
    current_account = Account(id=current_user.id, username=current_user.username, email=current_user.email)

    # Fetch all watched movie details for the current user
    watched_movie_details = current_account.get_watched_movies_by_user(current_account.id)

    imdb_score_min = request.args.get('imdb_score_min', default=None, type=float)
    imdb_score_max = request.args.get('imdb_score_max', default=None, type=float)

    num_votes_min = request.args.get('num_votes_min', default=None, type=int)

    genres = request.args.getlist('genres[]')  # Fetch multiple genre options
    language = request.args.get('selectedLanguage', default=None, type=str)

    # Fetch all watched movie details for the current user with filters
    watched_movie_details = get_filtered_watched_movies(
        user_db_config,
        current_user.id,
        imdb_score_min=imdb_score_min,
        imdb_score_max=imdb_score_max,

        num_votes_min=num_votes_min,
        genres=genres,
        language=language
    )

    # Get the sorting criteria from query parameters
    sort_by = request.args.get('sort_by', default='tconst', type=str)

    # Sort the movies using the imported function
    watched_movie_details = sort_movies(watched_movie_details, sort_by)

    if watched_movie_details is None or len(watched_movie_details) == 0:
        flash("No watched movies found for this user.")

    return render_template('watched_movies.html', watched_movie_details=watched_movie_details)


# @login_manager.user_loader
# def load_user(user_id):
#     # Query to fetch user details from the database
#     # user_data = execute_query(user_db_config, "SELECT * FROM users WHERE id=%s", (user_id,))
#     user_data = get_user_by_id(user_id)
#     # If user data exists, return a User object
#     if user_data:
#         return Account(id=user_data['id'], username=user_data['username'], email=user_data['email'])  # Add email here
#     # Otherwise, return None


# Declare a global variable to store the last displayed movie
global last_displayed_movie


@app.route('/previous_movie', methods=['GET', 'POST'])
def previous_movie():
    global current_displayed_movie, future_movies_stack  # Declare global variables

    # Append the current displayed movie to the future_movies_stack
    if current_displayed_movie is not None:
        future_movies_stack.append(current_displayed_movie)

    # Pop the previous movie from previous_movies_stack
    previous_movie_data = previous_movies_stack.pop()

    # Update the current displayed movie
    current_displayed_movie = previous_movie_data

    # Render the movie template, also passing the length of previous_movies_stack for UI control
    return render_template('movie.html',
                           movie=previous_movie_data,
                           current_user=current_user,
                           previous_count=len(previous_movies_stack))


@app.route('/next_movie', methods=['GET', 'POST'])
def next_movie():
    global current_displayed_movie  # Declare global variables

    # Append the current displayed movie to the previous_movies_stack
    if current_displayed_movie is not None:
        previous_movies_stack.append(current_displayed_movie)

    next_movie_data = None

    # Check if future_movies_stack has any movies to go forward to
    if future_movies_stack:
        next_movie_data = future_movies_stack.pop()
    else:
        # If no future movies, get a new movie from the queue
        next_movie_data = movie_queue.get()

    # Update the current displayed movie
    current_displayed_movie = next_movie_data

    # Render the movie template, also passing the length of previous_movies_stack for UI control
    return render_template('movie.html',
                           movie=next_movie_data,
                           current_user=current_user,
                           previous_count=len(previous_movies_stack))


# Assuming current_user is an instance of Account
@app.route('/seen_it', methods=['POST'])
@login_required
def seen_it():
    global current_displayed_movie
    if current_displayed_movie:
        tconst = current_displayed_movie.get("imdb_id")
        current_user.log_movie_to_user_account(current_user.id, current_user.username, tconst, current_displayed_movie,
                                               user_db_config)
        return redirect(url_for('movie'))
    else:
        return jsonify({'status': 'failure', 'message': 'No movies in the queue'}), 400


@user_logged_in.connect_via(app)
def on_user_logged_in(sender, user):
    # username = request.form['username']
    # password = request.form['password']
    #
    # user_data = Account.login_user(username, password, user_db_config)
    #
    # if user_data:
    #     # Create an Account instance for this user
    #     user = Account(id=user_data['id'], username=user_data['username'], email=user_data['email'])
    #
    pass


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         # Call the class method, passing in db_config explicitly
#         user_data = Account.login_user(username, password, user_db_config)
#
#         if user_data:
#             # Create an Account instance for this user
#             user = Account(id=user_data['id'], username=user_data['username'], email=user_data['email'])
#             login_user(user)
#             return redirect(url_for('home'))
#         else:
#             flash("Invalid username or password")
#
#     return render_template('security/login_user.html')


# # Route for logout
# @app.route('/logout')
# @login_required  # Require the user to be logged in to access this route
# def logout():
#     # Log the user out
#     logout_user()
#     # Redirect to the login page
#     return redirect(url_for('login'))
#

# # Route for user registration
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#
#         result = Account.register_user(username, email, password, user_db_config)
#
#         if result == "Username already exists.":
#             flash("Username already exists.")
#             return render_template('create_account_form.html')
#
#         flash("ShowModal")
#         return redirect(url_for('login'))
#
#     return render_template('create_account_form.html')
#

# Route for setting filters
@app.route('/setFilters')
def set_filters():
    print("entering setFilters")
    movie_queue_manager.stop_populate_thread()
    movie_queue_manager.empty_queue()
    movie_queue_manager.is_thread_alive()

    print(f"Current size of the movie queue: {movie_queue_manager.queue.qsize()}")

    # Render the filter settings template
    return render_template('set_filters.html')


@app.route('/add_to_watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    global current_displayed_movie  # Consider using a different state management approach
    if current_displayed_movie:
        tconst = current_displayed_movie.get("imdb_id")

        # Assuming current_user is an instance of Account
        current_user.add_movie_to_watchlist(current_user.id, current_user.username, tconst, current_displayed_movie,
                                            user_db_config)

        return redirect(url_for('movie'))
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
