import pymysql


def connect_to_db():
    # Replace the parameters below with your MySQL credentials
    host = 'localhost'
    user = 'root'
    password = 'caching_sha2_password'
    database = 'UserAccounts'

    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=database,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_user_by_id(user_id):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE id=%s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            return result
    finally:
        connection.close()


def get_user_by_username(username):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username=%s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            return result
    finally:
        connection.close()


def get_all_users():
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()


# Example usage
if __name__ == "__main__":
    user_by_id = get_user_by_id(1)
    print("User with ID 1:", user_by_id)

    user_by_username = get_user_by_username('john_doe')
    print("User with username 'john_doe':", user_by_username)

    all_users = get_all_users()
    print("All users:")
    for user in all_users:
        print(user)
