import imdb
import pymysql

from nextreel.models import User, WatchedMovies, UserWatchlist, db
from nextreel.scripts.movie import Movie


def get_user_login(username, password, user_datastore):
    user = user_datastore.find_user(username=username)
    if user and user_datastore.verify_password(password, user.password):
        return user
    else:
        return None


# The other functions would need to be modified similarly, replacing raw SQL queries with ORM operations.


def get_user_by_id(user_id):
    # Use the SQLAlchemy query API to get the user by ID
    return User.query.get(user_id)


def get_user_by_username(username):
    # Use the SQLAlchemy query API to get the user by username
    return User.query.filter_by(username=username).first()


def get_all_users():
    # Use the SQLAlchemy query API to get all users
    return User.query.all()


def get_watched_movie_posters(user_id):
    # Query WatchedMovie and join with Movie to get the poster URLs
    watched_movies = WatchedMovies.query.filter_by(user_id=user_id).join(Movie).all()
    return [{'url': wm.movie.poster_url, 'tconst': wm.tconst} for wm in watched_movies]


def get_watched_movies(user_id):
    # Query WatchedMovie to get the watched movies for a user
    watched_movies = WatchedMovies.query.filter_by(user_id=user_id).all()
    return [wm.tconst for wm in watched_movies]


def get_all_watched_movie_details_by_user(user_id):
    watched_movies = (
        db.session.query(WatchedMovies)
        .join(Movie, WatchedMovies.tconst == Movie.tconst)  # Explicit ON clause
        .filter(WatchedMovies.user_id == user_id)
        .all()
    )
    return watched_movies

def get_watched_movie_details(tconst):
    # Query Movie to get details of a movie by tconst
    return Movie.query.get(tconst)


def get_all_movies_in_watchlist(user_id):
    # Assuming you have a Watchlist model defined
    watchlist_movies = UserWatchlist.query.filter_by(user_id=user_id).join(Movie).all()
    return [transform_movie_details(wm.movie) for wm in watchlist_movies]


# Now, the transform_movie_details function will operate on Movie model instances
def transform_movie_details(movie):
    """
    Helper function to transform a Movie model instance into a dictionary
    """
    return {
        'tconst': movie.tconst,
        'title': movie.title,
        'genres': movie.genres,
        'directors': movie.directors,
        'writers': movie.writers,
        'runtimes': movie.runtimes,
        'rating': movie.rating,
        'votes': movie.votes,
        'poster_url': movie.poster_url
    }
