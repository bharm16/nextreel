from mysql_query_builder import execute_query
from db_config_scripts import db_config, user_db_config

def get_user_by_id(user_id):
    return execute_query(user_db_config, "SELECT * FROM users WHERE id=%s", (user_id,))

def get_user_by_username(username):
    return execute_query(user_db_config, "SELECT * FROM users WHERE username=%s", (username,))

def get_all_users():
    return execute_query(user_db_config, "SELECT * FROM users", fetch='all')

def insert_new_user(username, email, password):
    existing_user = execute_query(user_db_config, "SELECT * FROM users WHERE username=%s", (username,))
    if existing_user:
        return "Username already exists."

    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    execute_query(user_db_config, query, (username, email, password), fetch='none')

    # If you need the newly created user ID, you'd need to execute another query to fetch it.
    new_user = execute_query(user_db_config, "SELECT * FROM users WHERE username=%s", (username,))

    return {"message": f"User created successfully with ID {new_user['id']}.", "id": new_user['id']}

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
