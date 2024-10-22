import json
import pytest
from server.server import app
from database import database  # Import your database module

@pytest.fixture
def client():
    """Create a test client using Flask's test_client and initialize the database"""
    database.create_table()  # Ensure the table is created before each test
    # Clear existing data and reset the id sequence
    conn = database.get_db_connection()
    conn.execute('DELETE FROM items')  # Clear the table
    conn.execute('DELETE FROM sqlite_sequence WHERE name="items"')  # Reset the auto-increment
    conn.commit()
    conn.close()

    with app.test_client() as client:
        yield client

def test_get_request(client):
    """Test GET request to '/' route"""
    # First, insert some test data into the database
    database.insert_item("TestName1", "TestValue1")
    database.insert_item("TestName2", "TestValue2")

    response = client.get('/')
    assert response.status_code == 200

    # Convert response data to a dictionary
    response_data = json.loads(response.data)

    # Assert that the items retrieved are as expected
    expected_data = [
        {"id": 1, "name": "TestName1", "value": "TestValue1"},
        {"id": 2, "name": "TestName2", "value": "TestValue2"}
    ]
    assert response_data["items"] == expected_data

def test_post_request(client):
    """Test POST request to '/' route"""
    # Create a payload for the POST request
    data = {
        "name": "NewItem",
        "value": "NewValue"
    }

    response = client.post('/', json=data)
    assert response.status_code == 200

    # Convert response data to a dictionary
    response_data = json.loads(response.data)

    # Assert that the message and data received are correct
    assert response_data['message'] == "Item inserted"
    assert response_data['name'] == data['name']
    assert response_data['value'] == data['value']

    # Verify the item was inserted by making a GET request and checking the response
    get_response = client.get('/')
    get_response_data = json.loads(get_response.data)

    expected_data = [
        {"id": 1, "name": "NewItem", "value": "NewValue"}
    ]
    assert get_response_data["items"] == expected_data
