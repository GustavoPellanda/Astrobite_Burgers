import json
import pytest
from server.server import create_app

# Create a fixture to generate the app in a testing mode
@pytest.fixture
def client():
    app = create_app()  # Create the app using the factory function
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test to check if the index route is working
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Astrobite Burgers server up!" in response.data

# Test to check if the all burgers route is working
def test_get_all_burgers(client):
    response = client.get('/allBurgers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)  # Checks if the response is a list

# Test to check if the insert burger route is working
def test_insert_burger(client):
    new_burger = {
        "name": "Test Burger",
        "price": 9.99,
        "ingredients": ["lettuce", "tomato", "cheese"]
    }
    response = client.post('/newBurger', json=new_burger)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Burger added successfully"

# Test to check if the top burgers route is working
def test_get_top_burgers(client):
    response = client.get('/topBurgers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)  # Checks if the response is a list

# Test to check if the search burger route is working
def test_search_burger(client):
    new_burger = {
        "name": "Search Burger",
        "price": 7.99,
        "ingredients": ["bacon", "cheddar", "onions"]
    }
    client.post('/newBurger', json=new_burger)

    response = client.get('/searchBurger?name=Search Burger')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "Search Burger"
    assert data["price"] == 7.99
    
    # Check if the ingredients are returned correctly
    returned_ingredients = data["ingredients"].split(", ") if isinstance(data["ingredients"], str) else data["ingredients"]
    assert returned_ingredients == ["bacon", "cheddar", "onions"]

# Test to check if the update burger route is working
def test_update_burger(client):
    new_burger = {
        "name": "Update Burger",
        "price": 8.99,
        "ingredients": ["lettuce", "tomato", "pickles"]
    }
    response = client.post('/newBurger', json=new_burger)

    updated_burger = {
        "id": response.json.get("id"),
        "name": "Updated Burger",
        "price": 10.99,
        "ingredients": ["lettuce", "tomato", "bacon", "cheese"]
    }
    response = client.put('/updateBurger', json=updated_burger)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Burger updated successfully"

# Test to check if the delete burger route is working
def test_delete_burger(client):
    new_burger = {
        "name": "Delete Burger",
        "price": 5.99,
        "ingredients": ["onions", "cheddar", "bbq sauce"]
    }
    response = client.post('/newBurger', json=new_burger)
    burger_id = response.json.get("id")

    response = client.delete('/deleteBurger', json={"id": burger_id})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Burger deleted successfully"

