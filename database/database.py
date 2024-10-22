import sqlite3

# Create a connection to the SQLite database
# (This will create the database file if it doesn't exist)
def get_db_connection():
    conn = sqlite3.connect('data.db')  # 'data.db' is the database file
    conn.row_factory = sqlite3.Row     # Enable name-based access to columns
    return conn

# Function to create a table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to retrieve all items from the table
def get_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to insert a new item into the table
def insert_item(name, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, value) VALUES (?, ?)', (name, value))
    conn.commit()
    conn.close()
