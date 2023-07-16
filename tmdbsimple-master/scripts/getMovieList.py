import tmdbsimple as tmdb

API_KEY = '1ce9398920594a5521f0d53e9b33c52f'  # Replace 'your_api_key' with your actual TMDB API key
# API_KEY = 'k_0vtefojw'
tmdb.API_KEY = API_KEY

discover = tmdb.Discover()

# Use the movie method with vote_average_gte parameter
response = discover.movie(page=2, vote_average_gte=5)

if response:
    print(response)
else:
    print("No results found")
