
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

delete_query="""DELETE t1 from spotify_tracks t1
JOIN spotify_tracks t2 
ON
  t1.track_name=t2.track_name AND
  t1.album=t2.album AND
  t1.artist=t2.artist AND
  t1.popularity=t2.popularity AND
  t1.duration_minutes = t2.duration_minutes AND
  t1.id > t2.id;
"""
cursor.execute(delete_query)
connection.commit()
cursor.close()
connection.close()
print(f'Duplicates tracks removed from the database')

#if we want to truncate the table
#truncate_query="""TRUNCATE TABLE spotify_tracks"""
# cursor.execute(truncate_query)
# connection.commit()
# cursor.close()
# connection.close()
# print(fTable datas truncated successfully!')
