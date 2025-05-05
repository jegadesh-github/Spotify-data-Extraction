import mysql.connector
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import _mysql_connector

sp=spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='6f9dcb59b70c46a588d5f2b300d639d6',
    client_secret='fde88152da554ed38b662ecc1f8689dc'
))
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password123!',
    'database': 'spotify_db'
}
connection=mysql.connector.connect(**db_config)
cursor=connection.cursor()

alter_query={
    """
    ALTER table spotify_tracks
    ADD CONSTRAINT unique_track_entry
    UNIQUE (track_name, artist, album,popularity,duration_minutes);
    """
}
connection.commit()
cursor.close()
connection.close()

print("Unique constraint added successfully.")