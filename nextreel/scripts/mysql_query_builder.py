import pymysql


def execute_query(db_config, query, params=None, fetch='one'):
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

    cursor.close()
    conn.close()
    return result
