import pymysql

def get_titles_by_type(db_config, title_type):
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

    try:
        with connection.cursor() as cursor:
            # Query the title.basics table to get rows based on titleType
            cursor.execute("SELECT * FROM `title.basics` WHERE titleType = %s LIMIT 1", (title_type,))
            titles = cursor.fetchall()

        return titles
    finally:
        connection.close()

# Example usage
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}

title_types = ["movie", "short", "tvseries", "tvepisode", "video"]
for ttype in title_types:
    titles = get_titles_by_type(db_config, ttype)
    print(f"Titles of type {ttype}:")
    for title in titles:
        print(title)
    print("\n")
