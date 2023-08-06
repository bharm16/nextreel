from setFilters import get_random_row_value, get_rating_by_tconst, get_filtered_random_row

# Sample database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}


def test_random_row_value():
    row = get_random_row_value(db_config, 'title.basics', 'tconst')
    # print("Random Row Value:")
    # print(row)
    # print("-" * 50)


def test_rating_by_tconst():
    tconst = 'tt0331619'  # Sample tconst for testing
    rating = get_rating_by_tconst(db_config, tconst)
    # print(f"Rating for {tconst}:")
    # print(rating)
    # print("-" * 50)


def test_filtered_random_row():
    min_year = 2000
    max_year = 2020
    min_rating = 7.5
    max_rating = 10
    title_type = 'movie'  # This is optional, as the function defaults to 'movie'
    row = get_filtered_random_row(db_config, min_year, max_year, min_rating, max_rating, title_type)
    print(f"Random Row Value meeting all criteria:")
    print(row)
    print("-" * 50)


if __name__ == "__main__":
    test_random_row_value()
    test_rating_by_tconst()
    test_filtered_random_row()
