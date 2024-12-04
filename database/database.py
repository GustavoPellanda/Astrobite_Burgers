import sqlite3

DB_NAME = 'astrobite_burgers.db'

class Database:
    def __init__(self):
        self.db_name = DB_NAME
    
    def get_db_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Makes rows accessible by column name
        return conn
    
    def create_table(self):
        conn = self.get_db_connection()
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

    def insert_burger(self, name, price, ingredients):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO burgers (name, price, ingredients) VALUES (?, ?, ?)
        ''', (name, price, ', '.join(ingredients)))  # Ingredients are stored as a comma-separated string
        conn.commit()
        conn.close()

    def get_all_burgers(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM burgers')
        burgers = cursor.fetchall()
        conn.close()
        return [dict(burger) for burger in burgers]

    def get_top_burgers(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM burgers ORDER BY price DESC LIMIT 5')
        top_burgers = cursor.fetchall()
        conn.close()
        return [dict(burger) for burger in top_burgers]

    def search_burger(self, name):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM burgers WHERE name = ?', (name,))
        burger = cursor.fetchone()
        conn.close()
        return dict(burger) if burger else None

    def update_burger(self, id, name, price, ingredients):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE burgers
            SET name = ?, price = ?, ingredients = ?
            WHERE id = ?
        ''', (name, price, ', '.join(ingredients), id))
        conn.commit()
        conn.close()

    def delete_burger(self, id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM burgers WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def delete_all_burgers(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM burgers")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='burgers'")  # Reset the auto-increment counter
        conn.commit()
        conn.close()

    def update_burger_ids(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Retrieve all current burgers
        cursor.execute('SELECT id, name, price, ingredients FROM burgers')
        burgers = cursor.fetchall()

        # Update the IDs
        for new_id, (old_id, name, price, ingredients) in enumerate(burgers, start=1):
            cursor.execute('UPDATE burgers SET id = ? WHERE id = ?', (new_id, old_id))

        conn.commit()
        conn.close()
