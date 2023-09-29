from nextreel.scripts.mysql_query_builder import execute_query


class ImdbRandomMovieFetcher:
    def __init__(self, db_config):
        """Initialize with database configuration."""
        self.db_config = db_config

    def build_base_query(self):
        """Construct the base SQL query for fetching a random row."""
        return """
        SELECT tb.*
        FROM `title.basics` tb
        JOIN `title.ratings` tr ON tb.tconst = tr.tconst
        JOIN `title.akas` ta ON tb.tconst = ta.titleId
        WHERE tb.startYear BETWEEN %s AND %s
        AND tr.averagerating BETWEEN %s AND %s
        AND tr.numVotes >= %s
        AND tb.titleType = %s
        AND ta.language = %s
        """

    def build_parameters(self, criteria):
        """Construct the list of parameters for the SQL query based on given criteria."""
        parameters = [
            criteria.get('min_year', 1900),
            criteria.get('max_year', 2023),
            criteria.get('min_rating', 7.0),
            criteria.get('max_rating', 10),
            criteria.get('min_votes', 100000),
            criteria.get('title_type', 'movie'),
            criteria.get('language', 'en')
        ]
        return parameters

    def build_genre_conditions(self, criteria, parameters):
        """Construct the genre conditions for the SQL query."""
        genre_conditions = []
        genres = criteria.get('genres')
        if genres:
            genre_conditions = [" OR ".join(["tb.genres LIKE %s" for _ in genres])]
            parameters.extend(["%" + genre + "%" for genre in genres])
        return genre_conditions

    def fetch_random_movie(self, criteria):
        """Fetch a random movie row based on given criteria."""

        # Build the base query, parameters, and genre conditions
        base_query = self.build_base_query()
        parameters = self.build_parameters(criteria)
        genre_conditions = self.build_genre_conditions(criteria, parameters)

        # Complete the query by appending the genre conditions, if any
        full_query = base_query + (
            f" AND ({genre_conditions[0]})" if genre_conditions else "") + " ORDER BY RAND() LIMIT 1"

        # Debugging lines to print the generated SQL query and parameters
        print("Generated SQL Query:", full_query)
        print("Query Parameters:", parameters)

        # Execute the query and fetch the random row
        random_row = execute_query(self.db_config, full_query, parameters)

        return random_row if random_row else None


# Example usage
if __name__ == "__main__":
    db_config = {'host': 'localhost', 'user': 'root', 'password': 'password', 'database': 'imdb'}
    criteria = {'min_year': 2000, 'max_year': 2020, 'min_rating': 7, 'max_rating': 10, 'min_votes': 10000,
                'title_type': 'movie', 'language': 'en', 'genres': ['Action', 'Drama']}

    fetcher = ImdbRandomMovieFetcher(db_config)
    random_row = fetcher.fetch_random_movie(criteria)
    print("Random Movie Row:", random_row)
