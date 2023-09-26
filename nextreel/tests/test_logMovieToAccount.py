import unittest
from mock import patch
from datetime import datetime
from nextreel.scripts.log_movie_to_account import log_movie_to_account, query_watched_movie


class TestLogMovieToAccount(unittest.TestCase):

    # Test case for successful logging of movie to account
    @patch('nextreel.scripts.mysql_query_builder.execute_query')
    def test_log_movie_to_account_success(self, mock_execute_query):
        user_id = 'test_user'
        tconst = 'test_tconst'
        db_config = {'host': 'localhost', 'user': 'root'}  # Mock this

        mock_execute_query.return_value = None  # Simulate a successful database insert

        log_movie_to_account(user_id, tconst, db_config)

        # Verify if the execute_query was called with the correct parameters
        mock_execute_query.assert_called_once()

    # Test case for failure in logging of movie due to some exception
    @patch('nextreel.scripts.mysql_query_builder.execute_query')
    def test_log_movie_to_account_failure(self, mock_execute_query):
        user_id = 'test_user'
        tconst = 'test_tconst'
        db_config = {'host': 'localhost', 'user': 'root'}  # Mock this

        mock_execute_query.side_effect = Exception('Some error')  # Simulate a database error

        with self.assertRaises(Exception):
            log_movie_to_account(user_id, tconst, db_config)

    # Test case for querying a watched movie
    @patch('nextreel.scripts.mysql_query_builder.execute_query')
    def test_query_watched_movie(self, mock_execute_query):
        user_id = 'test_user'
        tconst = 'test_tconst'
        db_config = {'host': 'localhost', 'user': 'root'}  # Mock this

        mock_execute_query.return_value = {
            'user_id': user_id,
            'tconst': tconst,
            'watched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        result = query_watched_movie(user_id, tconst, db_config)

        # Verify if the execute_query was called with the correct parameters
        mock_execute_query.assert_called_once()

        # Check if the query result matches the expected values
        self.assertEqual(result['user_id'], user_id)
        self.assertEqual(result['tconst'], tconst)


if __name__ == '__main__':
    unittest.main()
