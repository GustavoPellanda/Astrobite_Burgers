from flask import Flask, request, jsonify
from database import database

app = Flask(__name__)

# Create the table when the server starts
database.create_table()

@app.route('/', methods=['GET'])
def index():
    return 'Astrobite Burguers server up!'

# Each burger has an ID, a name, a price, and a list of ingredients

@app.route('/allBurgers', methods=['GET'])
def get_all_burgers():
    burgers = database.get_all_burgers()
    return jsonify(burgers)

@app.route('/topBurgers', methods=['GET'])
def get_top_burgers():
    top_burgers = database.get_top_burgers()
    return jsonify(top_burgers)

@app.route('/searchBurger', methods=['GET'])
def search_burger():
    name = request.args.get('name')
    burger = database.search_burger(name)
    return jsonify(burger)

@app.route('/newBurger', methods=['POST']) # (admin)
def insert_burger():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    ingredients = data.get('ingredients')
    database.insert_burger(name, price, ingredients)
    return jsonify({'message': 'Burger added successfully'})

@app.route('/updateBurger', methods=['PUT']) # (admin)
def update_burger():
    data = request.json
    id = data.get('id')
    name = data.get('name')
    price = data.get('price')
    ingredients = data.get('ingredients')
    database.update_burger(id, name, price, ingredients)
    return jsonify({'message': 'Burger updated successfully'})

@app.route('/deleteBurger', methods=['DELETE']) # (admin)
def delete_burger():
    data = request.json
    id = data.get('id')
    database.delete_burger(id)
    return jsonify({'message': 'Burger deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)