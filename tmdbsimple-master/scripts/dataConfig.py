# import pandas as pd
#
# # Load data
# df = pd.read_csv('IMDb data files/title.basics.tsv', sep='\t', na_values='\\N', low_memory=False)
#
# # Format arrays
# # Assuming df is your DataFrame and 'genres' is the column with the issue
#
# # Transform the 'genres' column into the correct format
# df['genres'] = df['genres'].apply(lambda x: '{' + x + '}' if pd.notnull(x) else x)
#
#
# # Save data
# df.to_csv('title.basics.processedAgain.tsv', sep='\t', index=False, na_rep='NULL')


import json
import csv

# Open (or create) a CSV file and write the data
with open('data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    first_line = True

    # Open the JSON file
    with open('movie_ids_07_15_2023.json', 'r') as json_file:
        for line in json_file:
            data = json.loads(line)

            # Write the header if it's the first line
            if first_line:
                writer.writerow(data.keys())
                first_line = False

            # Write the data row
            writer.writerow(data.values())
