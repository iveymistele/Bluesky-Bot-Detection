import duckdb

con = duckdb.connect('bluesky.duckdb')

# Write to parquet using SQL

'''
con.execute("""
COPY post_features 
TO 'data/post_features.parquet' 
(FORMAT PARQUET)
""")
'''

con.execute("""
COPY account_features 
TO 'data/account_features.parquet' 
(FORMAT PARQUET)
""")