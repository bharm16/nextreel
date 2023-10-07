from flask_login import UserMixin

from nextreel.scripts.get_user_account import insert_new_user, get_user_login, get_all_watched_movie_details_by_user, \
    get_all_movies_in_watchlist
from nextreel.scripts.log_movie_to_account import add_movie_to_watchlist, log_movie_to_account


class Account(UserMixin):

    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    @classmethod
    def register_user(cls, username, email, password, db_config):
        return insert_new_user(username, email, password)

    @classmethod
    def login_user(cls, username, password, db_config):
        return get_user_login(username, password, db_config)

    def get_watched_movies_by_user(self, user_id):
        return get_all_watched_movie_details_by_user(user_id)

    def get_movies_in_watchlist(self, user_id):
        return get_all_movies_in_watchlist(user_id)

    def add_movie_to_watchlist(self, user_id, username, tconst, movie_data, db_config):
        return add_movie_to_watchlist(user_id, username, tconst, movie_data, db_config)

    def log_movie_to_user_account(self, user_id, username, tconst, movie_data, db_config):
        return log_movie_to_account(user_id, username, tconst, movie_data, db_config)
