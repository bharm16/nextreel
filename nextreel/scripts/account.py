from flask_security import current_user
from nextreel.scripts.get_user_account import get_all_watched_movie_details_by_user, get_all_movies_in_watchlist
from nextreel.scripts.log_movie_to_account import add_movie_to_watchlist, log_movie_to_account

class Account:
    # Since Flask-Security handles user details, you might not need this custom Account class anymore.
    # However, if you still need it for additional functionality, make sure it integrates properly with Flask-Security.

    def __init__(self, user=None):
        # If a user object is provided, use it; otherwise, use current_user from Flask-Security
        self.user = user or current_user

        # Ensure that self.user is not just a string by checking for the 'id' attribute
        if not hasattr(self.user, 'id'):
            raise TypeError("The provided user object does not have an 'id' attribute.")

    def get_watched_movies_by_user(self):
        # This method now relies on the 'id' of the user object
        return get_all_watched_movie_details_by_user(self.user.id)

    def get_movies_in_watchlist(self):
        # This method now relies on the 'id' of the user object
        return get_all_movies_in_watchlist(self.user.id)

    def add_movie_to_watchlist(self, tconst, movie_data, db_config):
        # This method now relies on the 'id' of the user object
        return add_movie_to_watchlist(self.user.id, tconst, movie_data, db_config)

    def log_movie_to_user_account(self, tconst, movie_data, db_config):
        # This method now relies on the 'id' of the user object
        return log_movie_to_account(self.user.id, tconst, movie_data, db_config)
