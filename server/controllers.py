from flask import jsonify
from server.services import BurgerService

class BurgerController:
    def __init__(self):
        self.burger_service = BurgerService()

    def get_all_burgers(self):
        burgers = self.burger_service.get_all_burgers()
        return jsonify(burgers)

    def get_top_burgers(self):
        top_burgers = self.burger_service.get_top_burgers()
        return jsonify(top_burgers)

    def search_burger(self, name):
        burger = self.burger_service.search_burger(name)
        return jsonify(burger)

    def insert_burger(self, data):
        self.burger_service.insert_burger(data)
        return jsonify({'message': 'Burger added successfully'})

    def insert_burgers(self, data):
        if not isinstance(data, list):
            return jsonify({'error': 'Invalid input format, expected a list of burgers.'}), 400

        burgers_added = self.burger_service.insert_burgers(data)
        return jsonify({'message': 'Burgers added successfully', 'burgers': burgers_added}), 200

    def update_burger(self, data):
        self.burger_service.update_burger(data)
        return jsonify({'message': 'Burger updated successfully'})

    def delete_burger(self, data):
        self.burger_service.delete_burger(data)
        return jsonify({'message': 'Burger deleted successfully'})

    def delete_all_burgers(self):
        self.burger_service.delete_all_burgers()
        return jsonify({'message': 'All burgers deleted successfully'})
