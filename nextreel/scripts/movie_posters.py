import os
import json
import pymysql
import pandas as pd


# Function to read image names and parse IMDb ID and score
def get_image_data(image_folder):
    image_data = {}
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg"):
            score, imdb_id = filename[:-4].split("_")
            image_data[imdb_id] = {"score": float(score), "image_url": filename}
    return image_data


# Database credentials
db_username = "root"
db_password = "caching_sha2_password"
db_name = "imdb"
db_host = "localhost"
db_port = 3306

# Create a connection
connection = pymysql.connect(host=db_host, user=db_username, password=db_password, database=db_name, port=db_port)

# Create a cursor
cursor = connection.cursor()

# Fetch existing data into a DataFrame
sql_query = "SELECT * FROM `title.basics`"
existing_df = pd.read_sql(sql_query, connection)

print(f"Number of rows in existing data: {len(existing_df)}")

# Read CSV data into a DataFrame
csv_filepath = '/Users/bryceharmon/Desktop/archive_a/MovieGenre.csv'
csv_df = pd.read_csv(csv_filepath, encoding='ISO-8859-1')


print(f"Number of rows in CSV data: {len(csv_df)}")

# Convert 'imdbId' to string to make it compatible with 'tconst' in existing_df
csv_df['imdbId'] = csv_df['imdbId'].apply(str)

# Merge both DataFrames on IMDb ID ('tconst' and 'imdbId')
merged_df = pd.merge(existing_df, csv_df, how='left', left_on='tconst', right_on='imdbId')

print(f"Number of rows in merged data: {len(merged_df)}")

updated_count = 0

# Loop through the DataFrame and update missing poster URLs
for index, row in merged_df.iterrows():
    imdb_id = row['tconst']
    existing_poster_url = row['poster_url']  # Assuming 'poster_url' is the column name for existing poster URLs

    if pd.isna(existing_poster_url):
        new_poster_url = row['Poster']

        if pd.notna(new_poster_url):  # If new_poster_url is not null
            sql_update_query = "UPDATE `title.basics` SET poster_url = %s WHERE tconst = %s"
            cursor.execute(sql_update_query, (new_poster_url, imdb_id))
            print(f"Row updated: {imdb_id} now has poster URL {new_poster_url}")
            updated_count += 1
        else:
            print(f"No new poster URL found for {imdb_id}.")
    else:
        print(f"Existing poster URL found for {imdb_id}.")

# Print the total number of updated rows
print(f"Total number of rows updated: {updated_count}")


# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
