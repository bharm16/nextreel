from bs4 import BeautifulSoup
from urllib.parse import quote

from tmdbsimple.imdbAPIAdvancedSearch import AdvancedSearchInput

# Your HTML string here
html = """
<!-- Your HTML here -->
"""

# Create a BeautifulSoup object
soup = BeautifulSoup(html, 'html.parser')

# Create an instance of AdvancedSearchInput
search_input = AdvancedSearchInput()

# Find release date inputs
release_date_min = soup.find('input', {'name': 'release_date-min'})
release_date_max = soup.find('input', {'name': 'release_date-max'})

# Assign the values to the search_input instance
if release_date_min and release_date_max:
    search_input.release_date_from = release_date_min.get('value')
    search_input.release_date_to = release_date_max.get('value')

# Find user rating inputs
user_rating_min = soup.find('select', {'name': 'user_rating-min'})
user_rating_max = soup.find('select', {'name': 'user_rating-max'})

# Assign the values to the search_input instance
if user_rating_min and user_rating_max:
    search_input.user_rating_from = user_rating_min.get('value')
    search_input.user_rating_to = user_rating_max.get('value')

# Find number of votes inputs
num_votes_min = soup.find('input', {'name': 'num_votes-min'})
num_votes_max = soup.find('input', {'name': 'num_votes-max'})

# Assign the values to the search_input instance
if num_votes_min and num_votes_max:
    search_input.number_of_votes_from = num_votes_min.get('value')
    search_input.number_of_votes_to = num_votes_max.get('value')

# Find genre checkboxes
genres = soup.find_all('input', {'name': 'genres'})

# Extract control id and label for each checkbox
genre_list = []
for genre in genres:
    if genre.get('checked'):
        genre_list.append(quote(genre.get('value')))

# Join all genres into a single string separated by commas
search_input.genres = ','.join(genre_list)

# Generate the query string
query_string = search_input.to_query_string()

# Print the query string
print(query_string)
