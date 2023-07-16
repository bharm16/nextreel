

import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Read the TSV file
df = pd.read_csv('IMDb data files/title.ratings.tsv.gz', sep='\t', compression='gzip')

# Create a database engine
engine = create_engine('postgresql://bryceharmon:bears2017@localhost:5432/IMDB_INFO')

# Create the table and load data
df.to_sql('imdb_titles', engine, if_exists='replace')
