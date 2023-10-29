import tmdbsimple as tmdb

from nextreel.scripts.movie import fetch_images_from_tmdb

# Initialize API Key
tmdb.API_KEY = '1ce9398920594a5521f0d53e9b33c52f'


# Function to fetch TMDb ID using IMDb tconst
def get_tmdb_id_by_tconst(tconst):
    find = tmdb.Find(tconst)
    response = find.info(external_source='imdb_id')
    tmdb_id = response['movie_results'][0]['id'] if response['movie_results'] else None
    return tmdb_id


# Function to fetch movie information by TMDb ID
def get_movie_info_by_tmdb_id(tmdb_id):
    movie = tmdb.Movies(tmdb_id)
    response = movie.info()
    return response


# Function to fetch cast information by TMDb ID
def get_cast_info_by_tmdb_id(tmdb_id):
    movie = tmdb.Movies(tmdb_id)
    response = movie.credits()
    return response.get('cast', [])


# Function to get full image URL
def get_full_image_url(profile_path, size='original'):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}{profile_path}"


# Function to get a backdrop image for the homepage
# Function to get a backdrop image for the homepage
def get_backdrop_image_for_home(tmdb_id):
    # Check if a corresponding TMDb ID exists
    if tmdb_id:
        # Use the fetch_images_from_tmdb function to get image data
        image_data = fetch_images_from_tmdb(tmdb_id)

        # Check if there are any backdrop images
        backdrops = image_data.get('backdrops', [])

        # If backdrop images exist, return the first one (or a random one if you prefer)
        if backdrops:
            backdrop_url = get_full_image_url(backdrops[0])  # Using the first backdrop image
            return backdrop_url
    return None


# Class for managing TMDb movie information
class TmdbMovieInfo:
    def __init__(self, api_key):
        self.api_key = api_key
        tmdb.API_KEY = self.api_key


# Main function
def main(api_key, tconst):
    # Initialize TMDb info
    tmdb_info = TmdbMovieInfo(api_key)

    # Fetch TMDb ID
    tmdb_id = get_tmdb_id_by_tconst(tconst)

    if tmdb_id:
        # Fetch and display movie information
        movie_info = get_movie_info_by_tmdb_id(tmdb_id)
        print("Movie Information from TMDb:", movie_info)

        # Fetch and display cast information
        cast_info = get_cast_info_by_tmdb_id(tmdb_id)
        print("Cast Information:")
        for cast_member in cast_info:
            print(f"{cast_member['name']} as {cast_member['character']}")

            # Fetch and display cast image URL
            profile_path = cast_member.get('profile_path')
            if profile_path:
                image_url = get_full_image_url(profile_path)
                print(f"Image URL: {image_url}")
            else:
                print("Image not available")

            # Fix here: pass tmdb_id instead of movie_info to get the backdrop image

        backdrop = get_backdrop_image_for_home(tmdb_id)
        print(backdrop)


    else:
        print("TMDb ID not found.")


# Example usage
if __name__ == "__main__":
    api_key = '1ce9398920594a5521f0d53e9b33c52f'  # Replace with your actual TMDb API key
    tconst = 'tt0111161'  # Replace with the IMDb tconst you have
    main(api_key, tconst)
