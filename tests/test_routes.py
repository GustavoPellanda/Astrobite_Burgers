import json
import pytest
from server.server import app
from database import database

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Astrobite Burguers server up!" in response.data

def test_get_all_burgers(client):
    response = client.get('/allBurgers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)  # Verifica se a resposta é uma lista

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
