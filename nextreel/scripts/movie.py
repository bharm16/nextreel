import imdb
import tmdbsimple as tmdb

from nextreel.scripts.db_config_scripts import db_config
from nextreel.scripts.mysql_query_builder import get_db_connection
from nextreel.scripts.set_filters_for_nextreel_backend import ImdbRandomMovieFetcher

get_db_connection(db_config)

# Initialize TMDb API Key
tmdb.API_KEY = '1ce9398920594a5521f0d53e9b33c52f'  # Replace with your actual TMDb API key


def get_tmdb_id_by_tconst(tconst):
    find = tmdb.Find(tconst)
    response = find.info(external_source='imdb_id')
    return response['movie_results'][0]['id'] if response['movie_results'] else None


def get_cast_info_by_tmdb_id(tmdb_id):
    movie = tmdb.Movies(tmdb_id)
    response = movie.credits()
    return response.get('cast', [])


def get_full_image_url(profile_path, size='w185'):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}{profile_path}"


class Movie:
    def __init__(self, tconst, db_config):
        self.tconst = tconst
        self.db_config = db_config
        self.movie_data = {}

    def fetch_info_from_imdb(self):
        """Fetch movie information from IMDb using IMDbPY."""
        imdbId = int(self.tconst[2:])
        ia = imdb.IMDb()
        return ia.get_movie(imdbId)

    def store_movie_data(self, movie):
        ia = imdb.IMDb()

        # Fetch cast information from IMDb
        imdb_cast = [actor['name'] for actor in movie.get('cast', [])][:3]

        # Fetch TMDb ID
        tmdb_id = get_tmdb_id_by_tconst(self.tconst)

        # Fetch cast information from TMDb
        tmdb_cast_info = []
        if tmdb_id:
            tmdb_cast = get_cast_info_by_tmdb_id(tmdb_id)[:3]  # Limit to first 3 actors
            for cast_member in tmdb_cast:
                profile_path = cast_member.get('profile_path')
                image_url = get_full_image_url(profile_path) if profile_path else None
                tmdb_cast_info.append({
                    'name': cast_member['name'],
                    'image_url': image_url
                })

        # Combine IMDb and TMDb cast information
        combined_cast = [{
            'name': name,
            'image_url': next((info['image_url'] for info in tmdb_cast_info if info['name'] == name), None)
        } for name in imdb_cast]

        self.movie_data = {
            "title": movie.get('title', 'N/A'),
            "imdb_id": movie.getID(),
            "genres": ', '.join(movie.get('genres', ['N/A'])),
            "directors": ', '.join([director['name'] for director in movie.get('director', [])]),
            "writers": next((writer['name'] for writer in movie.get('writer', []) if 'name' in writer), "N/A"),
            "cast": ', '.join([actor['name'] for actor in movie.get('cast', [])][:3]),
            "runtimes": ', '.join(movie.get('runtimes', ['N/A'])),
            "countries": ', '.join(movie.get('countries', ['N/A'])),
            "languages": movie.get('languages', ['N/A'])[0] if movie.get('languages') else 'N/A',
            # "languages": ', '.join(movie.get('languages', ['N/A'])) if movie.get('languages') else 'N/A',
            "rating": movie.get('rating', 'N/A'),
            "votes": movie.get('votes', 'N/A'),
            "plot": movie.get('plot', ['N/A'])[0],
            "poster_url": movie.get_fullsizeURL(),
            "year": movie.get('year'),
            "cast": combined_cast  # Combined cast information

        }

    def get_movie_data(self):
            movie_data = self.fetch_info_from_imdb()
            self.store_movie_data(movie_data)
            return self.movie_data

    # Main function to run the program
def main(criteria):
    movie_fetcher = ImdbRandomMovieFetcher(db_config)
    row = movie_fetcher.fetch_random_movie(criteria)

    if not row:
        print("No movies found based on the given criteria.")
        return None

    movie = Movie(row['tconst'], db_config)
    movie_data = movie.get_movie_data()
    print(movie_data)

    print("Fetched movie genres:", movie_data.get('genres'))

    # Example usage
if __name__ == "__main__":
    criteria = {
        "min_year": 1900,
        "max_year": 2023,
        "min_rating": 7.0,
        "max_rating": 10,
        "title_type": "movie",
        "language": "en",
        "genres": ["Action", "Drama"]
    }

    main(criteria)