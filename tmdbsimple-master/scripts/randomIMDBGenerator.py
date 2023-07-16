import psycopg2
import random


def get_db_connection():
    conn = psycopg2.connect(
        database="imdb_info",
        user="bryceharmon",
        password="bears2017",
        host="localhost",  # or the IP address of your database server
        port="5432"  # or the port number your database server is listening on
    )
    return conn


def execute_sql_query(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows


def execute_sql_query_with_random_tconst(sql_template):
    # Connect to the database
    conn = get_db_connection()

    rows = []

    # Keep generating tconst values and executing the SQL query until we get some rows
    while not rows:
        # Generate a random tconst
        start = 1
        end = 9916880
        random_number = random.randint(start, end)
        random_number_str = str(random_number).zfill(7)
        random_tconst = 'tt' + random_number_str

        # Format the SQL query with the random tconst
        sql = sql_template.format(tconst=random_tconst)

        # Execute the SQL query
        rows = execute_sql_query(conn, sql)
        if rows is None:  # Add this check
            rows = []

    # Print the result
    for row in rows:
        print(row)

    # Close the database connection
    conn.close()


sql_template = """
    SELECT
        tb.tconst,
        tb.titleType,
        tb.primaryTitle,
        tb.originalTitle,
        tb.isAdult,
        tb.startYear,
        tb.runtimeMinutes,
        tb.genres,
        tr.averageRating,
        tr.numVotes
    FROM
        imdb_info.public.title_basics AS tb
    INNER JOIN
        imdb_info.public.title_ratings AS tr ON tb.tconst = tr.tconst
    WHERE
        tb.tconst = '{tconst}' AND tb.titleType = 'movie';
"""


execute_sql_query_with_random_tconst(sql_template)
