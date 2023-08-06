import pymysql
import random


def get_db_connection(db_config):
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )


def get_random_row_value(db_config, table_name, column_name):
    with get_db_connection(db_config) as connection:
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
            cursor.execute("SELECT * FROM `{}` WHERE {} = %s".format(table_name, column_name), (random_value,))
            random_row = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]

        return dict(zip(column_names, random_row))


def get_rating_by_tconst(db_config, tconst):
    with get_db_connection(db_config) as connection:
        with connection.cursor() as cursor:
            # Fetch the rating information based on the tconst
            cursor.execute("SELECT * FROM `title.ratings` WHERE tconst = %s", (tconst,))
            rating_info = cursor.fetchone()

        return rating_info


def get_filtered_random_row(db_config, min_year, max_year, min_rating, max_rating, title_type='movie'):
    with get_db_connection(db_config) as connection:
        with connection.cursor() as cursor:
            # Construct the query to fetch a random row that meets all the criteria
            query = """
            SELECT tb.* 
            FROM `title.basics` tb
            JOIN `title.ratings` tr ON tb.tconst = tr.tconst
            WHERE tb.startYear >= %s AND tb.startYear <= %s 
            AND tr.averagerating >= %s AND tr.averagerating <= %s 
            AND tb.titleType = %s
            ORDER BY RAND() LIMIT 1
            """
            cursor.execute(query, (min_year, max_year, min_rating, max_rating, title_type))
            random_row = cursor.fetchone()
            column_names = [desc[0] for desc in cursor.description]

        return dict(zip(column_names, random_row))


# You can include any other utility functions or code as needed.
