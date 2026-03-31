import duckdb
from datetime import datetime

def log(message):
    """Print a timestamped status message to stdout.

    Args:
        message: Text to print.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

try:
    con = duckdb.connect('bluesky.duckdb')
    log("Connected to DuckDB")

    try:
        con.execute("""
        COPY post_features 
        TO 'data/post_features.parquet' 
        (FORMAT PARQUET)
        """)
        log("Exported post_features to Parquet")
    except Exception as e:
        log(f"Failed to export post_features: {e}")

    try:
        con.execute("""
        COPY account_features 
        TO 'data/account_features.parquet' 
        (FORMAT PARQUET)
        """)
        log("Exported account_features to Parquet")
    except Exception as e:
        log(f"Failed to export account_features: {e}")

except Exception as e:
    log(f"Database connection failed: {e}")

finally:
    try:
        con.close()
        log("Closed DuckDB connection")
    except:
        pass