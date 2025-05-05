import re
import mysql.connector
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from mysql.connector import errorcode

# Spotify API setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='6f9dcb59b70c46a588d5f2b300d639d6',
    client_secret='fde88152da554ed38b662ecc1f8689dc'
))
# file_path = "track_urls.txt"
# with open(file_path, "r") as file:
#     track_urls = file.readlines()
# MySQL DB config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password123!',
    'database': 'spotify_db'
}
track_urls=['https://open.spotify.com/track/4UBJXetaoB06Crk0kENmxP?si=27f065760c074367',
            'https://open.spotify.com/track/0HFVSbqv9Dr3jSrvkaa5JD?si=2f05592cb89946bc']
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()
insert_query = """
INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""

for url in track_urls:
    try:
        track_id = re.search(r'track/([a-zA-Z0-9]+)', url).group(1)
        track = sp.track(track_id)

        track_data = {
            'Track Name': track['name'],
            'Artist': track['artists'][0]['name'],
            'Album': track['album']['name'],
            'Popularity': track['popularity'],
            'Duration (minutes)': track['duration_ms'] / 60000
        }

        cursor.execute(insert_query, (
            track_data['Track Name'],
            track_data['Artist'],
            track_data['Album'],
            track_data['Popularity'],
            track_data['Duration (minutes)']
        ))
        print(f"Track '{track_data['Track Name']}' by {track_data['Artist']} inserted into database.")


    except mysql.connector.Error as err:

        if err.errno == errorcode.ER_DUP_ENTRY:

            print(f"Duplicate found: {track_data['Track Name']} — Skipped.")

        else:
            print(f"MySQL Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

connection.commit()
cursor.close()
connection.close()

print("Tracks insertion process completed.")
