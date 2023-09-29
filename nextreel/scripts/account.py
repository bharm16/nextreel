# Import required modules
# ... (Your existing imports)
from nextreel.scripts.db_config_scripts import user_db_config
from nextreel.scripts.get_user_account import get_all_watched_movie_details_by_user, get_all_movies_in_watchlist, \
    insert_new_user, get_user_login
from nextreel.scripts.log_movie_to_account import add_movie_to_watchlist, log_movie_to_account


# Create a UserAccountManager class to handle all user-related functionalities
class Account:

    def __init__(self, user_db_config):
        self.user_db_config = user_db_config

    def get_watched_movies_by_user(self, user_id):
        return get_all_watched_movie_details_by_user(user_id)

    def get_movies_in_watchlist(self, user_id):
        return get_all_movies_in_watchlist(user_id)

    def add_movie_to_watchlist(self, user_id, username, tconst, movie_data):
        return add_movie_to_watchlist(user_id, username, tconst, movie_data, self.user_db_config)

    def log_movie_to_user_account(self, user_id, username, tconst, movie_data):
        return log_movie_to_account(user_id, username, tconst, movie_data, self.user_db_config)

    # Add more methods as needed...

    def register_user(self, username, email, password):
        # Insert the new user into the database
        # Assuming insert_new_user function returns a status message
        return insert_new_user(username, email, password)

    def login_user(self, username, password):
        # Fetch and verify user details
        # Assuming get_user_login function returns user data if login is successful, otherwise None
        return get_user_login(username, password, self.user_db_config)


# Initialize an instance of UserAccountManager
account = Account(user_db_config)
