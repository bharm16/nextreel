import random

import imdb
import tmdbsimple as tmdb
from nextreel.scripts.db_config_scripts import db_config
from nextreel.scripts.mysql_query_builder import get_db_connection
from nextreel.scripts.set_filters_for_nextreel_backend import ImdbRandomMovieFetcher

# Initialize database connection
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


def get_video_url_by_tmdb_id(tmdb_id):
    """
    Fetches a single video URL for a movie from TMDb using its TMDb ID.
    It looks for a video that is on YouTube and is of type "Trailer".

    Args:
        tmdb_id (int): The TMDb ID of the movie.

    Returns:
        str: A single video URL, or None if no suitable video is found.
    """
    movie = tmdb.Movies(tmdb_id)
    response = movie.videos()
    video_results = response.get('results', [])

    for video in video_results:
        # Only include videos that are on YouTube and are of type "Trailer"
        if video['site'] == 'YouTube' and video['type'] == 'Trailer':
            youtube_url = f"https://www.youtube.com/watch?v={video['key']}"
            return youtube_url  # Return the first suitable video URL found

    return None  # Return None if no suitable video is found


def fetch_images_from_tmdb(tmdb_id):
    """
    Fetch movie images from TMDb using the movie's TMDb ID.

    Args:
        tmdb_id (int): The TMDb ID of the movie.

    Returns:
        dict: A dictionary containing image URLs.
    """
    movie = tmdb.Movies(tmdb_id)
    response = movie.images()
    image_data = {
        'posters': [img['file_path'] for img in response.get('posters', [])],
        'backdrops': [img['file_path'] for img in response.get('backdrops', [])]
    }
    return image_data


def fetch_videos_from_tmdb(tmdb_id):
    """
    Fetch movie videos from TMDb using the movie's TMDb ID.

    Args:
        tmdb_id (int): The TMDb ID of the movie.

    Returns:
        list: A list of dictionaries containing video data.
    """
    movie = tmdb.Movies(tmdb_id)
    response = movie.videos()  # Fetch video data from TMDb
    return response.get('results', [])  # Extract the 'results' field which contains the video data


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
        tmdb_id = get_tmdb_id_by_tconst(self.tconst)
        tmdb_cast_info = []
        if tmdb_id:

            tmdb_movie_trailer = get_video_url_by_tmdb_id(tmdb_id)

            tmdb_cast = get_cast_info_by_tmdb_id(tmdb_id)[:10]  # Limit to first 10 actors
            for cast_member in tmdb_cast:
                profile_path = cast_member.get('profile_path')
                image_url = get_full_image_url(profile_path) if profile_path else None
                tmdb_cast_info.append({
                    'name': cast_member['name'],
                    'image_url': image_url
                })
            tmdb_image_info = fetch_images_from_tmdb(tmdb_id)

        self.movie_data = {
            "title": movie.get('title', 'N/A'),
            "imdb_id": movie.getID(),
            "genres": ', '.join(movie.get('genres', ['N/A'])),
            "directors": ', '.join([director['name'] for director in movie.get('director', [])]),
            "writers": next((writer['name'] for writer in movie.get('writer', []) if 'name' in writer), "N/A"),
            "runtimes": ', '.join(movie.get('runtimes', ['N/A'])),
            "countries": ', '.join(movie.get('countries', ['N/A'])),
            "languages": movie.get('languages', ['N/A'])[0] if movie.get('languages') else 'N/A',
            "rating": movie.get('rating', 'N/A'),
            "votes": movie.get('votes', 'N/A'),
            "plot": movie.get('plot', ['N/A'])[0],
            "poster_url": movie.get_fullsizeURL(),
            "year": movie.get('year'),
            "cast": tmdb_cast_info,
            "images": tmdb_image_info,  # Add TMDb image information
            "trailer": tmdb_movie_trailer  # Add TMDb video URLs

        }

    def get_movie_data(self):
        movie_data = self.fetch_info_from_imdb()
        self.store_movie_data(movie_data)
        return self.movie_data


def get_random_backdrop_url(backdrops):
    """
    Selects a random backdrop URL from a list of backdrops.

    Args:
        backdrops (list): List of backdrop image file paths.

    Returns:
        str: The full URL of a randomly selected backdrop, or None if no backdrops are available.
    """
    if backdrops:
        random_backdrop = random.choice(backdrops)  # Randomly select a backdrop
        return get_full_image_url(random_backdrop)  # You can specify the size you want
    else:
        return None


def main(criteria):
    movie_fetcher = ImdbRandomMovieFetcher(db_config)
    row = movie_fetcher.fetch_random_movie(criteria)

    if not row:
        print("No movies found based on the given criteria.")
        return None

    movie = Movie(row['tconst'], db_config)
    movie_data = movie.get_movie_data()
    print(movie_data)

    # Corrected this line
    for image in movie_data["images"].get('posters', []):
        print(image)



        # New code to randomly select a backdrop
    random_backdrop_url = get_random_backdrop_url(movie_data["images"].get('backdrops', []))
    if random_backdrop_url:
        print(f"Randomly selected backdrop URL: {random_backdrop_url}")
    else:
        print("No backdrops available for this movie.")

    print(movie_data.get("trailer", []))


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
