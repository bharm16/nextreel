import pandas as pd

# Load data
df = pd.read_csv('IMDb data files/title.basics.tsv', sep='\t', na_values='\\N', low_memory=False)

# Format arrays
# Assuming df is your DataFrame and 'genres' is the column with the issue

# Transform the 'genres' column into the correct format
df['genres'] = df['genres'].apply(lambda x: '{' + x + '}' if pd.notnull(x) else x)


# Save data
df.to_csv('title.basics.processedAgain.tsv', sep='\t', index=False, na_rep='NULL')
