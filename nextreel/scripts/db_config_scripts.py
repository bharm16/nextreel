import pymysql

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'imdb'
}

user_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'UserAccounts'
}


def show_create_statements_for_all_tables(db_config):
    try:
        # Connecting to the database
        conn = pymysql.connect(**db_config)
        print(f"Connected to database: {db_config['database']}")

        cursor = conn.cursor()

        # Showing tables only in imdb database
        cursor.execute("SHOW TABLES IN imdb")
        tables = cursor.fetchall()

        print(f"Tables found: {tables}")

        for table in tables:
            table_name = table[0]
            print(f"Current table name: {table_name}")  # Debug print

            query = f"SHOW CREATE TABLE `imdb`.`{table_name}`"  # Enclose table name in backticks
            print(f"Executing query: {query}")  # Debug print

            cursor.execute(query)
            create_table_statement = cursor.fetchone()[1]

            print(f"Create Table Statement for {table_name}:\n{create_table_statement}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()
        conn.close()


# Show CREATE TABLE statements
show_create_statements_for_all_tables(db_config)



def show_create_statements_for_all_tables_in_user_accounts(db_config):
    try:
        # Connecting to the database
        conn = pymysql.connect(**db_config)
        # print(f"Connected to database: {db_config['database']}")

        cursor = conn.cursor()

        # Show tables only in the UserAccounts database
        cursor.execute("SHOW TABLES IN UserAccounts")
        tables = cursor.fetchall()

        # print(f"Tables found: {tables}")

        for table in tables:
            table_name = table[0]
            # print(f"Current table name: {table_name}")  # Debug print

            query = f"SHOW CREATE TABLE `UserAccounts`.`{table_name}`"  # Enclose table name in backticks
            # print(f"Executing query: {query}")  # Debug print

            cursor.execute(query)
            create_table_statement = cursor.fetchone()[1]

            # print(f"Create Table Statement for {table_name}:\n{create_table_statement}\n")
            print(f" {table_name}:\n{create_table_statement}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cursor.close()
        conn.close()

# Example usage

# Fetch and display the CREATE TABLE statements
# show_create_statements_for_all_tables_in_user_accounts(user_db_config)
