import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
DB_NAME = 'astrobite_burgers.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS burgers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            ingredients TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_burger(name, price, ingredients):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO burgers (name, price, ingredients) VALUES (?, ?, ?)
    ''', (name, price, ', '.join(ingredients)))  # Ingredients are stored as a comma-separated string
    conn.commit()
    conn.close()

def get_all_burgers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM burgers')
    burgers = cursor.fetchall()
    conn.close()
    return [dict(burger) for burger in burgers]  # Return a list of dictionaries

def get_top_burgers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM burgers ORDER BY price DESC LIMIT 5')
    top_burgers = cursor.fetchall()
    conn.close()
    return [dict(burger) for burger in top_burgers]

def search_burger(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM burgers WHERE name = ?', (name,))
    burger = cursor.fetchone()
    conn.close()
    return dict(burger) if burger else None

def update_burger(id, name, price, ingredients):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE burgers
        SET name = ?, price = ?, ingredients = ?
        WHERE id = ?
    ''', (name, price, ', '.join(ingredients), id))
    conn.commit()
    conn.close()

def delete_burger(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM burgers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
