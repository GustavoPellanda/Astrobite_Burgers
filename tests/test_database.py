import pytest
import sqlite3
from database.database import (
    create_table,
    insert_burger,
    get_all_burgers,
    get_top_burgers,
    search_burger,
    update_burger,
    delete_burger,
    get_db_connection
)

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')  # In-memory database for tests
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

# Fixture to initialize the table for testing
@pytest.fixture
def setup_table(db_connection):
    create_table()
    yield
    cursor = db_connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS burgers')
    db_connection.commit()

def test_insert_burger(db_connection, setup_table):
    insert_burger(db_connection, "Classic Burger", 5.99, ["beef", "lettuce", "tomato"])
    burgers = get_all_burgers(db_connection)
    assert len(burgers) == 1
    assert burgers[0]["name"] == "Classic Burger"
    assert burgers[0]["price"] == 5.99
    assert burgers[0]["ingredients"] == "beef, lettuce, tomato"

def test_get_all_burgers(db_connection, setup_table):
    insert_burger(db_connection, "Veggie Burger", 4.99, ["lettuce", "tomato", "cheese"])
    insert_burger(db_connection, "Chicken Burger", 6.49, ["chicken", "lettuce", "tomato"])
    burgers = get_all_burgers(db_connection)
    assert len(burgers) == 2

def test_get_top_burgers(db_connection, setup_table):
    insert_burger(db_connection, "Burger A", 8.99, ["beef", "cheese"])
    insert_burger(db_connection, "Burger B", 7.99, ["chicken", "lettuce"])
    insert_burger(db_connection, "Burger C", 6.99, ["veggie", "lettuce", "tomato"])
    top_burgers = get_top_burgers(db_connection)
    assert len(top_burgers) == 3
    assert top_burgers[0]["price"] == 8.99

def test_update_burger(db_connection, setup_table):
    insert_burger(db_connection, "Old Burger", 4.99, ["beef", "lettuce"])
    burger = search_burger(db_connection, "Old Burger")
    update_burger(db_connection, burger["id"], "Updated Burger", 5.99, ["beef", "cheese"])
    updated_burger = search_burger(db_connection, "Updated Burger")
    assert updated_burger is not None
    assert updated_burger["name"] == "Updated Burger"
    assert updated_burger["price"] == 5.99

def test_delete_burger(db_connection, setup_table):
    insert_burger("Temp Burger", 5.49, ["beef", "onion"])
    burger = search_burger("Temp Burger")
    delete_burger(burger["id"])
    deleted_burger = search_burger("Temp Burger")
    assert deleted_burger is None
