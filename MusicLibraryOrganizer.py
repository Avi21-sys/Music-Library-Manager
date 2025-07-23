import sqlite3

# Connect or create the database
conn = sqlite3.connect('music.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT,
        album TEXT,
        genre TEXT,
        year INTEGER,
        file_path TEXT
    )
''')
conn.commit()

# Function to add a new song
def add_song():
    title = input("Enter song title: ")
    artist = input("Enter artist name: ")
    album = input("Enter album name: ")
    genre = input("Enter genre: ")
    year = input("Enter year: ")
    file_path = input("Enter audio file path: ")

    cursor.execute('''
        INSERT INTO songs (title, artist, album, genre, year, file_path)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, artist, album, genre, year, file_path))
    conn.commit()
    print("✅ Song added successfully.")

# Function to update song details
def update_song():
    song_id = input("Enter song ID to update: ")
    print("Leave fields blank to keep current value.")
    title = input("New title: ")
    artist = input("New artist: ")
    album = input("New album: ")
    genre = input("New genre: ")
    year = input("New year: ")
    file_path = input("New file path: ")

    # Fetch current record
    cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
    record = cursor.fetchone()
    if not record:
        print("❌ Song not found.")
        return

    # Use new value or keep old
    title = title or record[1]
    artist = artist or record[2]
    album = album or record[3]
    genre = genre or record[4]
    year = year or record[5]
    file_path = file_path or record[6]

    cursor.execute('''
        UPDATE songs
        SET title = ?, artist = ?, album = ?, genre = ?, year = ?, file_path = ?
        WHERE id = ?
    ''', (title, artist, album, genre, year, file_path, song_id))
    conn.commit()
    print("✅ Song updated successfully.")

# Function to search songs
def search_songs():
    keyword = input("Enter keyword to search (title/artist/album): ")
    cursor.execute('''
        SELECT * FROM songs
        WHERE title LIKE ? OR artist LIKE ? OR album LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    results = cursor.fetchall()
    
    if results:
        print("\n🎵 Search Results:")
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]}")
    else:
        print("❌ No matching songs found.")

# Function to view all songs
def view_all_songs():
    cursor.execute("SELECT * FROM songs")
    rows = cursor.fetchall()
    if rows:
        print("\n🎼 Music Library:")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]}")
    else:
        print("Library is empty.")

# Function to delete a song
def delete_song():
    song_id = input("Enter song ID to delete: ")
    cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))
    conn.commit()
    print("🗑️ Song deleted (if existed).")

# CLI Menu
def main():
    while True:
        print("\n==== Personal Music Library ====")
        print("1. Add New Song")
        print("2. Update Song Info")
        print("3. Search Songs")
        print("4. View All Songs")
        print("5. Delete Song")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ")
        
        if choice == '1':
            add_song()
        elif choice == '2':
            update_song()
        elif choice == '3':
            search_songs()
        elif choice == '4':
            view_all_songs()
        elif choice == '5':
            delete_song()
        elif choice == '6':
            print("👋 Exiting Music Library.")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
    conn.close()
