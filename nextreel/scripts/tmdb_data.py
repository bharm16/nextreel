import tmdbsimple as tmdb

tmdb.API_KEY = '1ce9398920594a5521f0d53e9b33c52f'

movie = tmdb.Movies(603)
response = movie.info()

print(response)

tconst = movie.external_ids()

print(tconst)



def get_tmdb_id_by_tconst(tconst):
    """Fetch TMDb ID using IMDb tconst."""
    find = tmdb.Find(tconst)
    response = find.info(external_source='imdb_id')
    tmdb_id = response['movie_results'][0]['id'] if response['movie_results'] else None
    return tmdb_id


def get_movie_info_by_tmdb_id(tmdb_id):
    """Fetch movie information by TMDb ID."""
    movie = tmdb.Movies(tmdb_id)
    response = movie.info()
    return response


class TmdbMovieInfo:
    def __init__(self, api_key):
        self.api_key = api_key
        tmdb.API_KEY = self.api_key


# Main function to run the program
def main(api_key, tconst):
    tmdb_info = TmdbMovieInfo(api_key)

    # Fetch TMDb ID using IMDb tconst
    tmdb_id = get_tmdb_id_by_tconst(tconst)

    if tmdb_id:
        # Fetch and print movie information by TMDb ID
        movie_info = get_movie_info_by_tmdb_id(tmdb_id)
        print("Movie Information from TMDb:", movie_info)
    else:
        print("TMDb ID not found.")


# Example usage
if __name__ == "__main__":
    api_key = '1ce9398920594a5521f0d53e9b33c52f'  # Replace with your actual TMDb API key
    tconst = 'tt0111161'  # Replace with the IMDb tconst you have
    main(api_key, tconst)
