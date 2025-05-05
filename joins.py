import mysql.connector

# Database connection setup
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password123!',
    'database': 'spotify_db'
}

# Connect to MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Step 1: Create second table
create_artist_table = """
CREATE TABLE IF NOT EXISTS artist_details (
    artist_name VARCHAR(100),
    genre VARCHAR(100),
    country VARCHAR(100)
)
"""
cursor.execute(create_artist_table)

# Step 2: Insert data into artist_details
insert_artist_data = """
INSERT IGNORE INTO artist_details (artist_name, genre, country) VALUES 
('Vijay', 'Playback Pop', 'India'),
('Chinmayi', 'Classical Pop', 'India'),
('Karthik', 'Melody', 'India')
"""
cursor.execute(insert_artist_data)

# Step 3: INNER JOIN query
inner_join_query = """
SELECT t.track_name, t.artist, a.genre
FROM spotify_tracks t
JOIN artist_details a ON t.artist = a.artist_name
"""

cursor.execute(inner_join_query)
results = cursor.fetchall()

# Display the results
print("Track Name | Artist | Genre")
print("-" * 40)
for row in results:
    print(f"{row[0]} | {row[1]} | {row[2]}")

# Cleanup
connection.commit()
cursor.close()
connection.close()
