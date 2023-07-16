import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        database="imdb_info",
        user="bryceharmon",
        password="bears2017",
        host="localhost",
        port="5432"
    )
    return conn


def execute_sql_query(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows


def get_unique_genres(conn):
    # Execute a SQL query to fetch all genres
    rows = execute_sql_query(conn, "SELECT genres FROM title_basics WHERE titleType = 'movie'")

    # Create a set to store unique genres
    genres = set()

    # Iterate through each row
    for row in rows:
        # Genres are a list in this case, so we can directly iterate over them
        genres_in_row = row[0]
        # Add each genre to the set of unique genres
        for genre in genres_in_row:
            genres.add(genre)

    return genres


# Connect to the database
conn = get_db_connection()

# Fetch and print all unique genres
unique_genres = get_unique_genres(conn)
# for genre in unique_genres:
#print(genre)

# Close the database connection
conn.close()
