from pyexpat import features

import mysql.connector
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import spotipy
import matplotlib.pyplot as plt
import re


sp=spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='your client id',
    client_secret='your secret id'
))

track_url="https://open.spotify.com/track/6SZgnc7BvRmSXErk0hyXkq?si=ebc1144f7b344cfd"

track_id=re.search('track/([a-zA-Z0-9]+)',track_url).group(1)

track=sp.track(track_id)
print(track)

track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

print(f"\nTrack Name:{track_data['Track Name']}")
print(f"\nArtist:{track_data['Artist']}")
print(f"\nAlbum:{track_data['Album']}")
print(f"\nPopularity:{track_data['Popularity']}")
print(f"\nDuration:{track_data['Duration (minutes)']:.2f} minutes")

df=pd.DataFrame([track_data])
print("\n Track data as Dataframe:")
print(df.to_string())

df.to_csv('spotify_track_data.csv',index=False)

features=['Popularity','Duration (minutes)']
values=[track_data['Popularity'],track_data['Duration (minutes)']]

plt.figure(figsize=(5,4))
plt.bar(features,values,color='skyblue',edgecolor='red',width=0.2)
plt.title(f"Track Metadata for '{track_data['Track Name']}")
plt.ylabel('Value')
plt.show()
