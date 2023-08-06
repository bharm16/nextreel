import pymysql


def get_genres(db_config):
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

    try:
        with connection.cursor() as cursor:
            # Query the title.basics table to get the genre field
            cursor.execute("SELECT genres FROM `title.basics`")
            genres = cursor.fetchall()

        return genres
    finally:
        connection.close()


# Example usage
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}

genres = get_genres(db_config)
for genre in genres:
    print(genre[0])  # Print each genre
