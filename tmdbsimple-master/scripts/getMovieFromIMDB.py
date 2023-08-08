from .setFilters import get_filtered_random_row
import imdb  # make sure you have imported the imdb module

# Sample database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}


def get_movie_tconst():
    min_year = 2000
    max_year = 2020
    min_rating = 7.5
    max_rating = 10
    min_votes = 100000
    title_type = 'movie'  # This is optional, as the function defaults to 'movie'

    # Retrieve the row using the setFilters functions
    row = get_filtered_random_row(db_config, min_year, max_year, min_rating, max_rating, min_votes, title_type)

    return row['tconst']


if __name__ == "__main__":
    tconst = get_movie_tconst()

    # Extract the numeric ID from the tconst
    imdbId = int(tconst[2:])

    # Fetch the movie details using imdbpy
    ia = imdb.IMDb()
    movie = ia.get_movie(imdbId)
    print(f"Movie details for TCONST {tconst}:")
    print(movie)


    def display_movie_info(movie_obj):
        """
        Print all information related to a movie using the Movie class.
        :param movie_obj: Instance of the Movie class from IMDbPY.
        """
        # Check if the movie object is valid
        if not movie_obj:
            print("Invalid movie object!")
            return

        # Print movie details
        print("=" * 50)
        print(f"Title: {movie_obj.get('title', 'N/A')}")
        print(f"IMDb ID: {movie_obj.getID()}")
        print(f"Genres: {', '.join(movie_obj.get('genres', ['N/A']))}")
        print(f"Director(s): {', '.join([director['name'] for director in movie_obj.get('director', [])])}")
        print(f"Writer(s): {', '.join([writer['name'] for writer in movie_obj.get('writer', []) if 'name' in writer])}")
        print(f"Cast: {', '.join([actor['name'] for actor in movie_obj.get('cast', [])])}")
        print(f"Runtime(s): {', '.join(movie_obj.get('runtimes', ['N/A']))}")
        print(f"Country(s): {', '.join(movie_obj.get('countries', ['N/A']))}")
        print(f"Language(s): {', '.join(movie_obj.get('languages', ['N/A']))}")
        print(f"Rating: {movie_obj.get('rating', 'N/A')}")
        print(f"Number of Votes: {movie_obj.get('votes', 'N/A')}")
        print(f"Plot: {movie_obj.get('plot', ['N/A'])[0]}")

        # You can add more fields as needed.
        print("=" * 50)

    # Example usage:
    # Assuming 'movie' is an instance of the Movie class
    # display_movie_info(movie)
    print(display_movie_info(movie))


