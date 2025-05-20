# 🎵 Spotify Track Importer

A Python-based tool that **fetches track details from Spotify** using the Spotify API and **stores them in a MySQL database**. Supports automatic table creation, error handling, and easy database integration.

---

## 🚀 Features

✅ Extracts track details (Name, Artist, Album, Popularity, Duration)  
✅ Saves track data into a **MySQL database**  
✅ **Automatic table creation** (if `spotify_tracks` does not exist)  
✅ **Error handling** for database operations  
✅ Uses **Spotipy** for Spotify API access  

---

## 🔧 Setup Instructions

### **1️⃣ Install Dependencies**
Ensure you have Python installed, then run:

```bash
pip install mysql-connector-python spotipy
