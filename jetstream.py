import asyncio
import websockets
import json
import duckdb
from datetime import datetime

uri = "wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post"

log_file = open("ingestion.log", "a", encoding="utf-8")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    log_file.write(line + "\n")
    log_file.flush()

try:
    conn = duckdb.connect("bluesky.duckdb")
    log("Connected to DuckDB database")
except Exception as e:
    log(f"Failed to connect to DuckDB: {e}")
    raise

# Reset tables for a fresh run
conn.execute("DROP TABLE IF EXISTS posts")
conn.execute("DROP TABLE IF EXISTS accounts")

# Accounts table
conn.execute("""
CREATE TABLE accounts (
    did VARCHAR PRIMARY KEY,
    first_seen_at TIMESTAMP,
    last_seen_at TIMESTAMP,
    post_count BIGINT
)
""")

# Posts table
conn.execute("""
CREATE TABLE posts (
    id VARCHAR PRIMARY KEY,
    did VARCHAR,
    collection VARCHAR,
    rkey VARCHAR,
    text VARCHAR,
    created_at TIMESTAMP,
    is_reply BOOLEAN,
    raw_json VARCHAR
)
""")



def safe_parse_timestamp(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None

async def listen_to_websocket():
    async with websockets.connect(uri, max_size=None) as websocket:
        log("Connected to Jetstream")

        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)

                if data.get("kind") != "commit":
                    continue

                commit = data.get("commit", {})
                if commit.get("collection") != "app.bsky.feed.post":
                    continue

                record = commit.get("record", {})
                did = data.get("did")
                collection = commit.get("collection")
                rkey = commit.get("rkey")
                text = record.get("text")
                created_at = safe_parse_timestamp(record.get("createdAt"))
                is_reply = record.get("reply") is not None

                if not (did and collection and rkey):
                    log("Skipping event: missing post_id pieces")
                    continue

                post_id = f"at://{did}/{collection}/{rkey}"

                if not text:
                    log(f"Skipping empty-text post: {post_id}")
                    continue

                # Insert post if it does not already exist
                conn.execute("""
                    INSERT INTO posts (
                        id, did, collection, rkey, text, created_at, is_reply, raw_json
                    )
                    SELECT ?, ?, ?, ?, ?, ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM posts WHERE id = ?
                    )
                """, [
                    post_id,
                    did,
                    collection,
                    rkey,
                    text,
                    created_at,
                    is_reply,
                    message,
                    post_id
                ])

                # Upsert account summary
                conn.execute("""
                    INSERT INTO accounts (did, first_seen_at, last_seen_at, post_count)
                    VALUES (?, ?, ?, 1)
                    ON CONFLICT(did) DO UPDATE SET
                        first_seen_at = LEAST(accounts.first_seen_at, excluded.first_seen_at),
                        last_seen_at  = GREATEST(accounts.last_seen_at, excluded.last_seen_at),
                        post_count    = accounts.post_count + 1
                """, [did, created_at, created_at])

                log(f"Inserted post: {post_id}")

            except websockets.ConnectionClosed as e:
                log(f"Connection closed: {e}")
                break
            except Exception as e:
                log(f"Error: {e}")

def export_to_parquet():
    log("Exporting tables to Parquet...")
    conn.execute("COPY accounts TO 'accounts.parquet' (FORMAT PARQUET)")
    conn.execute("COPY posts TO 'posts.parquet' (FORMAT PARQUET)")
    log("Parquet export complete.")

if __name__ == "__main__":
    try:
        asyncio.run(listen_to_websocket())
    finally:
        export_to_parquet()
        conn.close()
        log_file.close()