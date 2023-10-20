# sort_and_filter.py
from nextreel.scripts.mysql_query_builder import execute_query


def sort_movies(watched_movie_details, sort_by='tconst'):
    """
    Sorts a list of watched movie details based on the provided criteria.
    """
    if not watched_movie_details:
        return []

    # Determine sorting column and order
    sort_column, sort_order = 'tconst', 'ASC'  # Default values
    if sort_by == 'year_low_to_high':
        sort_column, sort_order = 'year', 'ASC'
    elif sort_by == 'year_high_to_low':
        sort_column, sort_order = 'year', 'DESC'
    elif sort_by == 'imdb_low_to_high':
        sort_column, sort_order = 'rating', 'ASC'
    elif sort_by == 'imdb_high_to_low':
        sort_column, sort_order = 'rating', 'DESC'
    elif sort_by == 'vote_low_to_high':
        sort_column, sort_order = 'votes', 'ASC'
    elif sort_by == 'vote_high_to_low':
        sort_column, sort_order = 'votes', 'DESC'

    # Sort the movies
    watched_movie_details.sort(key=lambda x: x.get(sort_column, 0), reverse=(sort_order == 'DESC'))

    return watched_movie_details


# Query to fetch all watched movie details for a user with filters and sorting
GET_FILTERED_WATCHED_MOVIES = """
SELECT * FROM watched_movie_detail
WHERE user_id=%s
{}
{}
"""


# queries.py

# queries.py

def get_filtered_watched_movies(user_db_config, user_id, imdb_score_min=None, imdb_score_max=None, num_votes_min=None, genres=None,
                                language=None):
    """
    Fetch watched movies for a user based on filters.

    Parameters:
        user_db_config (dict): Database configuration for the user.
        user_id (int): The ID of the user.
        imdb_score_min (float): Minimum IMDB score filter.
        num_votes_min (int): Minimum number of votes filter.
        genres (list): List of genres to filter by.
        language (str): Language filter.

    Returns:
        list: List of watched movies based on the filters.
    """
    filter_clauses = []
    params = [user_id]  # Initialize with user_id as it will always be there

    # Add filter conditions based on the parameters
    if imdb_score_min is not None:
        filter_clauses.append(" AND rating >= %s")
        params.append(imdb_score_min)

    # Add filter conditions based on the parameters
    if imdb_score_max is not None:
        filter_clauses.append(" AND rating <= %s")
        params.append(imdb_score_max)

    if num_votes_min is not None:
        filter_clauses.append(" AND votes >= %s")
        params.append(num_votes_min)

    if genres:
        genre_conditions = " OR ".join(["genres LIKE %s" for _ in genres])
        filter_clauses.append(f" AND ({genre_conditions})")
        params.extend([f"%{genre}%" for genre in genres])

    if language:
        filter_clauses.append(" AND language = %s")
        params.append(language)

    # Finalize the SQL query by inserting the filter clauses
    final_query = GET_FILTERED_WATCHED_MOVIES.format("".join(filter_clauses), "")

    # Execute the query and fetch results
    return execute_query(user_db_config, final_query, params=params, fetch='all')
