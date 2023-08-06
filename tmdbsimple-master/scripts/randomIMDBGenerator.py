import pymysql
import random


def get_random_row_value(db_config, table_name, column_name):
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

    try:
        with connection.cursor() as cursor:
            # Find the total number of rows in the table
            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            total_rows = cursor.fetchone()[0]

            # Select a random row number
            random_row_num = random.randint(1, total_rows)

            # Fetch the value from the random row
            cursor.execute(f"SELECT {column_name} FROM `{table_name}` LIMIT {random_row_num - 1}, 1")
            random_value = cursor.fetchone()[0]

            # Fetch the entire row based on the random value
            cursor.execute(f"SELECT * FROM `{table_name}` WHERE {column_name} = %s", (random_value,))
            random_row = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]

        return dict(zip(column_names, random_row))
    finally:
        connection.close()


def get_rating_by_tconst(db_config, tconst):
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

    try:
        with connection.cursor() as cursor:
            # Fetch the rating information based on the tconst
            cursor.execute("SELECT * FROM `title.ratings` WHERE tconst = %s", (tconst,))
            rating_info = cursor.fetchone()

        return rating_info
    finally:
        connection.close()


# Example usage
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}
random_row = get_random_row_value(db_config, 'title.basics', 'tconst')
print(random_row)

tconst = random_row['tconst']
rating_info = get_rating_by_tconst(db_config, tconst)
print(f"Rating information for tconst {tconst}:")
print(rating_info)


def get_db_connection():
    conn = pymysql.connect(
        database="imdb",
        user="root",
        password="caching_sha2_password",
        host="localhost",
        port=3306
    )
    return conn
