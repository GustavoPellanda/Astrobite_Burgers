import sqlite3
from database.database import Database

# Set up the database and create the table
def setup_db():
    db = Database()
    db.db_name = ':memory:'  # Use in-memory database for testing
    db.create_table()
    return db

# Test inserting a burger
def test_insert_burger():
    db = setup_db()
    db.insert_burger('Cheeseburger', 5.99, ['cheese', 'beef', 'lettuce'])
    burgers = db.get_all_burgers()
    assert len(burgers) == 1
    assert burgers[0]['name'] == 'Cheeseburger'

# Test getting all burgers
def test_get_all_burgers():
    db = setup_db()
    db.insert_burger('Cheeseburger', 5.99, ['cheese', 'beef', 'lettuce'])
    db.insert_burger('Veggie Burger', 4.99, ['lettuce', 'tomato', 'cheese'])
    burgers = db.get_all_burgers()
    assert len(burgers) == 2

# Test deleting a burger
def test_delete_burger():
    db = setup_db()
    db.insert_burger('Cheeseburger', 5.99, ['cheese', 'beef', 'lettuce'])
    burgers = db.get_all_burgers()
    burger_id = burgers[0]['id']
    db.delete_burger(burger_id)
    burgers = db.get_all_burgers()
    assert len(burgers) == 0

# Test updating a burger
def test_update_burger():
    db = setup_db()
    db.insert_burger('Cheeseburger', 5.99, ['cheese', 'beef', 'lettuce'])
    burgers = db.get_all_burgers()
    burger_id = burgers[0]['id']
    db.update_burger(burger_id, 'Cheeseburger Deluxe', 6.99, ['cheese', 'beef', 'lettuce', 'bacon'])
    updated_burger = db.search_burger('Cheeseburger Deluxe')
    assert updated_burger['price'] == 6.99

# Test getting top burgers by price
def test_get_top_burgers():
    db = setup_db()
    db.insert_burger('Cheeseburger', 5.99, ['cheese', 'beef', 'lettuce'])
    db.insert_burger('Veggie Burger', 4.99, ['lettuce', 'tomato', 'cheese'])
    db.insert_burger('Deluxe Burger', 7.99, ['cheese', 'beef', 'lettuce', 'bacon'])
    top_burgers = db.get_top_burgers()
    assert len(top_burgers) == 3
    assert top_burgers[0]['name'] == 'Deluxe Burger'

# Run all tests
if __name__ == "__main__":
    test_insert_burger()
    test_get_all_burgers()
    test_delete_burger()
    test_update_burger()
    test_get_top_burgers()
    print("All tests passed.")
