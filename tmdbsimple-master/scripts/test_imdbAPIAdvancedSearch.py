from scripts.imdbAPIAdvancedSearch import AdvancedSearchInput

search_input = AdvancedSearchInput()
search_input.title = "The Matrix"
search_input.title_type = "movie"
search_input.user_rating_from = 7.5

base_url = "https://imdb-api.com/API/AdvancedSearch/"  # replace with your base URL


url = search_input.to_query_string()
print(url)
