import mysql.connector
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import re

sp=spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='your client id',
    client_secret='your secret id'
))

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password123!',
    'database': 'spotify_db'
}

# Connect to database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

track_url = "https://open.spotify.com/track/1qfanYrmrh7xDSvt15acZ3?si=e81e18cc5abe45e6"

track_id = re.search('track/([a-zA-Z0-9]+)', track_url).group(1)

track = sp.track(track_id)
print(track)

track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

insert_query = """
INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""


cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration (minutes)']
))

connection.commit()
print(f"Track '{track_data['Track Name']}' by {track_data['Artist']} inserted into database.")


cursor.close()
connection.close()
