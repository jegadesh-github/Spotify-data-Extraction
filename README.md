# 🎵 Spotify Track Importer

A Python-based tool that fetches track details from Spotify using the Spotify API and stores them in a MySQL database.

## 🚀 Features
- ✅ Extracts track details (Name, Artist(s), Album, Popularity, Duration)
- ✅ Saves track data into a MySQL database
- ✅ Automatic table creation (if `spotify_tracks` does not exist)
- ✅ Error handling with logging
- ✅ Secure credentials with `.env`
- ✅ Uses [Spotipy](https://spotipy.readthedocs.io/) for Spotify API access

## 🛠️ Tech Stack
- Python  
- Spotify API (Spotipy)  
- MySQL  
- dotenv  

## ⚙️ Setup & Usage
1. Clone this repo:
   ```bash
   git clone https://github.com/jegadesh-github/Spotify-data-Extraction.git
   cd Spotify-data-Extraction

2.Create a .env file in the root with your credentials:
  SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
DB_HOST=localhost
DB_USER=root
DB_PASS=your_password
DB_NAME=spotify_db
TRACK_URLS_FILE=track_urls.txt

3.Install dependencies:
 pip install -r requirements.txt

4.Add track URLs to track_urls.txt:
 https://open.spotify.com/track/7qiZfU4dY1lWllzX7mPBI3
 
5.Run the script:
 python spotify_mysql_urls.py

📊 Example Output
  INFO: Inserted: 'Shape of You' by Ed Sheeran
  INFO: All tracks processed.
