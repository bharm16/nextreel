from flask_security import current_user
from flask_login import UserMixin
from sqlalchemy.sql.functions import user

from nextreel.models import User
from nextreel.scripts.get_user_account import get_all_watched_movie_details_by_user, get_all_movies_in_watchlist
from nextreel.scripts.log_movie_to_account import add_movie_to_watchlist, log_movie_to_account


# Assuming the User class is defined elsewhere and is the model used by Flask-Security
# from your_app.models import User

class Account(User):
    # Since Flask-Security handles user details, you might not need this custom Account class anymore.
    # However, if you still need it for additional functionality, make sure it integrates properly with Flask-Security.

    def __init__(self, ):
        # Assuming 'user' is an instance of Flask-Security's User model
        self.user = user

    def get_watched_movies_by_user(self):
        # Use the Flask-Security current_user proxy
        return get_all_watched_movie_details_by_user(self.id)

    def get_movies_in_watchlist(self):
        # Use the Flask-Security current_user proxy
        return get_all_movies_in_watchlist(self.id)

    def add_movie_to_watchlist(self, tconst, movie_data, db_config):
        # Use the Flask-Security current_user proxy
        return add_movie_to_watchlist(self.id, self.user.username, tconst, movie_data, db_config)

    def log_movie_to_user_account(self, tconst, movie_data, db_config):
        # Use the Flask-Security current_user proxy
        return log_movie_to_account(self.id, self.user.username, tconst, movie_data, db_config)
