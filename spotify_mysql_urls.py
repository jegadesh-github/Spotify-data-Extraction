import os
import re
import logging
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector

# Load .env file if present
load_dotenv()

# -------------------------------
# Logging
# -------------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# -------------------------------
# Spotify Authentication (env vars)
# -------------------------------
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    logging.error("Spotify credentials not found. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env or environment.")
    raise SystemExit(1)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# -------------------------------
# Database Configuration (env vars)
# -------------------------------
db_config = {
    'host': os.getenv("DB_HOST", "localhost"),
    'user': os.getenv("DB_USER", "root"),
    'password': os.getenv("DB_PASS", ""),
    'database': os.getenv("DB_NAME", "spotify_db")
}

# -------------------------------
# Helpers
# -------------------------------
def get_track_id_from_url(url):
    url = url.strip()
    match = re.search(r'track/([A-Za-z0-9]+)', url)
    if match:
        return match.group(1)
    # fallback: last path segment (handles raw IDs or query params)
    return url.split('/')[-1].split('?')[0]

def connect_db():
    return mysql.connector.connect(**db_config)

# -------------------------------
# Main processing
# -------------------------------
def main():
    # Connect to DB
    try:
        conn = connect_db()
        cursor = conn.cursor()
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

    # Create DB if necessary (optional)
    # If your DB server doesn't have spotify_db, create it via CLI or uncomment the lines below.
    # cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(db_config['database']))
    # conn.database = db_config['database']

    # Create table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS spotify_tracks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        track_name VARCHAR(255),
        artist VARCHAR(255),
        album VARCHAR(255),
        popularity INT,
        duration_minutes FLOAT
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

    # Read track URLs
    file_path = os.getenv("TRACK_URLS_FILE", "track_urls.txt")
    if not os.path.exists(file_path):
        logging.error(f"Track URL file not found: {file_path}")
        cursor.close()
        conn.close()
        return

    with open(file_path, "r", encoding="utf-8") as f:
        track_urls = [line.strip() for line in f if line.strip()]

    for track_url in track_urls:
        try:
            track_id = get_track_id_from_url(track_url)
            track = sp.track(track_id)

            # join multiple artists
            artists = ", ".join([a['name'] for a in track.get('artists', [])])
            track_name = track.get('name')
            album = track.get('album', {}).get('name')
            popularity = track.get('popularity')
            duration_minutes = track.get('duration_ms', 0) / 60000.0

            insert_query = """
                INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (track_name, artists, album, popularity, duration_minutes))
            logging.info(f"Inserted: '{track_name}' by {artists}")

        except Exception as e:
            logging.error(f"Error processing URL: {track_url}. Error: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    logging.info("All tracks processed.")

if __name__ == "__main__":
    main()
