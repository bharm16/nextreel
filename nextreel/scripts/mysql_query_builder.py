from datetime import time
import time
import pymysql


def execute_query(db_config, query, params=None, fetch='one'):
    start_time = time.time()  # Start the timer

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute(query, params)

    if fetch == 'one':
        result = cursor.fetchone()
    elif fetch == 'all':
        result = cursor.fetchall()
    elif fetch == 'none':  # For queries like INSERT, UPDATE, DELETE
        conn.commit()
        result = None

    end_time = time.time()  # Stop the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time

    print(f"Execution time for query: {elapsed_time:.5f} seconds")

    cursor.close()
    conn.close()
    return result
