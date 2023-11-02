from nextreel.scripts.mysql_query_builder import execute_query


def build_parameters(criteria):
    """Construct the list of parameters for the SQL query based on given criteria."""
    # Note: Added "LIKE" clause for the language
    language = "%" + criteria.get('language', 'en') + "%"
    parameters = [
        criteria.get('min_year', 1900),
        criteria.get('max_year', 2023),
        criteria.get('min_rating', 7.0),
        criteria.get('max_rating', 10),
        criteria.get('min_votes', 100000),
        criteria.get('title_type', 'movie'),
        language  # added this line
    ]
    return parameters


def build_genre_conditions(criteria, parameters):
    """Construct the genre conditions for the SQL query."""
    genre_conditions = []
    genres = criteria.get('genres')
    if genres:
        genre_conditions = [" OR ".join(["tb.genres LIKE %s" for _ in genres])]
        parameters.extend(["%" + genre + "%" for genre in genres])
    return genre_conditions


def build_base_query():
    return """
  SELECT tb.*
    FROM `title.basics` tb
    JOIN `title.ratings` tr ON tb.tconst = tr.tconst
    WHERE tb.startYear BETWEEN %s AND %s
    AND tr.averagerating BETWEEN %s AND %s
    AND tr.numVotes >= %s
    AND tb.titleType = %s
    AND tb.language LIKE %s  -- Changed this line
    """


class ImdbRandomMovieFetcher:
    def __init__(self, db_config):
        """Initialize with database configuration."""
        self.db_config = db_config

    def fetch_random_movies25(self, criteria):
        """Fetch 25 random movie rows based on given criteria."""

        # Build the base query, parameters, and genre conditions
        base_query = build_base_query()
        parameters = build_parameters(criteria)
        genre_conditions = build_genre_conditions(criteria, parameters)

        # Debugging: Print the criteria and parameters
        print("Criteria passed to fetch_random_movie:", criteria)
        print("Parameters built for SQL query:", parameters)

        # Complete the query by appending the genre conditions, if any
        # Changed LIMIT 1 to LIMIT 25 to fetch 25 rows instead of 1
        full_query = base_query + (
            f" AND ({genre_conditions[0]})" if genre_conditions else "") + " ORDER BY RAND() LIMIT 25"

        # Debugging lines to print the generated SQL query and parameters
        print("Generated SQL Query:", full_query)
        print("Query Parameters:", parameters)

        # Execute the query and fetch the random rows
        random_rows = execute_query(self.db_config, full_query, parameters, fetch='all')

        # if random_rows:
        #     print("Fetched 25 random movies:")
        #     for i, row in enumerate(random_rows):
        #         print(f"Row {i + 1}: {row}")
        # else:
        #     print("No movies found based on the given criteria.")

        return random_rows if random_rows else None

    def fetch_random_movie(self, criteria):
        """Fetch a random movie row based on given criteria."""

        # Build the base query, parameters, and genre conditions
        base_query = build_base_query()
        parameters = build_parameters(criteria)
        genre_conditions = build_genre_conditions(criteria, parameters)

        # Debugging: Print the criteria and parameters
        print("Criteria passed to fetch_random_movie:", criteria)
        print("Parameters built for SQL query:", parameters)

        # Complete the query by appending the genre conditions, if any
        full_query = base_query + (
            f" AND ({genre_conditions[0]})" if genre_conditions else "") + " ORDER BY RAND() LIMIT 1"

        # Debugging lines to print the generated SQL query and parameters
        print("Generated SQL Query:", full_query)
        print("Query Parameters:", parameters)

        # Execute the query and fetch the random row
        random_row = execute_query(self.db_config, full_query, parameters)

        return random_row if random_row else None


def extract_movie_filter_criteria(form_data):
    """
    Extract filter criteria from the form data.



    Returns:
        dict: Dictionary containing the filter criteria.
    """

    # Initialize an empty criteria dictionary
    criteria = {}

    # Handling various other criteria (year, IMDb score, number of votes)
    if form_data.get('year_min'):
        criteria['min_year'] = int(form_data.get('year_min'))
    if form_data.get('year_max'):
        criteria['max_year'] = int(form_data.get('year_max'))
    if form_data.get('imdb_score_min'):
        criteria['min_rating'] = float(form_data.get('imdb_score_min'))
    if form_data.get('imdb_score_max'):
        criteria['max_rating'] = float(form_data.get('imdb_score_max'))
    if form_data.get('num_votes_min'):
        criteria['min_votes'] = int(form_data.get('num_votes_min'))

    # Handling genre criteria
    genres = form_data.getlist('genres[]')
    if genres:
        criteria['genres'] = genres

    # Handling language criteria
    if form_data.get('language'):
        criteria['language'] = form_data.get('language')
    else:
        print("defaulting to english")
        criteria['language'] = 'en'  # Default to English

    return criteria


# Example usage
if __name__ == "__main__":
    db_config = {'host': 'localhost',
                 'user': 'root',
                 'password': 'caching_sha2_password',
                 'database': 'imdb'}

    criteria = {'min_year': 2000,
                'max_year': 2020,
                'min_rating': 7,
                'max_rating': 10,
                'min_votes': 10000,
                'title_type': 'movie',
                'language': 'en',
                'genres': ['Action', 'Drama']}

    fetcher = ImdbRandomMovieFetcher(db_config)
    random_row = fetcher.fetch_random_movie(criteria)
    print("Random Movie Row:", random_row)

    # Test fetching 25 random movies
    random_rows = fetcher.fetch_random_movies25(criteria)

    # # Debugging: Print the fetched rows
    # if random_rows:
    #     print("Fetched 25 random movies:")
    #     for i, row in enumerate(random_rows):
    #         print(f"Row {i + 1}: {row}")
    # else:
    #     print("No movies found based on the given criteria.")
