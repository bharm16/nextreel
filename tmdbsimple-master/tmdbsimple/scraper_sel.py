from selenium import webdriver
from imdbAPIAdvancedSearch import AdvancedSearchInput

# Step 1: Load the HTML file
driver = webdriver.Chrome('/path/to/chromedriver')  # replace with the path to your ChromeDriver
driver.get('file:///path/to/your/file.html')  # replace with the path to your HTML file

# Step 2: Create an instance of AdvancedSearchInput
search_input = AdvancedSearchInput()

# Step 3: Interact with the HTML and scrape data
# (the following is just an example, you would need to adapt it to your needs)
title_input = driver.find_element_by_name('title')
search_input.title = title_input.get_attribute('value')

# Step 4: Use the scraped data
query_string = search_input.to_query_string()
print(query_string)

# Close the browser
driver.quit()
