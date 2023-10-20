# sort_and_filter.py

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
