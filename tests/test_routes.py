import json
import pytest
import time
import requests  # Use 'requests' to make actual HTTP requests to the Flask server

# Define the base URL for the Flask server running in Docker
BASE_URL = "http://localhost:5000"

@pytest.fixture
def client():
    # Wait for the Flask server to be fully ready (you can adjust this based on how long your server takes to start)
    for _ in range(10):
        try:
            # Make a request to check if the server is up and running
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(2)
    yield requests  # Use 'requests' to interact with the server
    # You can add teardown logic here if needed (e.g., shutting down the server)

def test_index_route(client):
    response = client.get(f'{BASE_URL}/')
    assert response.status_code == 200
    assert b"Astrobite Burguers server up!" in response.content

def test_get_all_burgers(client):
    response = client.get(f'{BASE_URL}/allBurgers')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Checks if the response is a list

def test_insert_burger(client):
    new_burger = {
        "name": "Test Burger",
        "price": 9.99,
        "ingredients": ["lettuce", "tomato", "cheese"]
    }
    response = client.post(f'{BASE_URL}/newBurger', json=new_burger)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Burger added successfully"

def test_get_top_burgers(client):
    response = client.get(f'{BASE_URL}/topBurgers')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Checks if the response is a list

def test_search_burger(client):
    # Insert a burger before searching, in case it doesn't exist
    new_burger = {
        "name": "Search Burger",
        "price": 7.99,
        "ingredients": ["bacon", "cheddar", "onions"]
    }
    client.post(f'{BASE_URL}/newBurger', json=new_burger)

    # Perform the search by name
    response = client.get(f'{BASE_URL}/searchBurger?name=Search Burger')
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Search Burger"
    assert data["price"] == 7.99
    returned_ingredients = data["ingredients"].split(", ") if isinstance(data["ingredients"], str) else data["ingredients"]
    assert returned_ingredients == ["bacon", "cheddar", "onions"]

def test_update_burger(client):
    # Insert a burger to be updated
    new_burger = {
        "name": "Update Burger",
        "price": 8.99,
        "ingredients": ["lettuce", "tomato", "pickles"]
    }
    response = client.post(f'{BASE_URL}/newBurger', json=new_burger)
    
    updated_burger = {
        "id": response.json().get("id"),
        "name": "Updated Burger",
        "price": 10.99,
        "ingredients": ["lettuce", "tomato", "bacon", "cheese"]
    }
    response = client.put(f'{BASE_URL}/updateBurger', json=updated_burger)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Burger updated successfully"

def test_delete_burger(client):
    # Insert a burger to delete
    new_burger = {
        "name": "Delete Burger",
        "price": 5.99,
        "ingredients": ["onions", "cheddar", "bbq sauce"]
    }
    response = client.post(f'{BASE_URL}/newBurger', json=new_burger)
    burger_id = response.json().get("id")
    
    response = client.delete(f'{BASE_URL}/deleteBurger', json={"id": burger_id})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Burger deleted successfully"
