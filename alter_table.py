import mysql.connector
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import _mysql_connector

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
