from flask import jsonify
from server.services import BurgerService

class BurgerController:
    def __init__(self):
        self.burger_service = BurgerService()

    def get_all_burgers(self):
        try:
            burgers = self.burger_service.get_all_burgers()
            return jsonify(burgers)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_top_burgers(self):
        try:
            top_burgers = self.burger_service.get_top_burgers()
            return jsonify(top_burgers)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def search_burger(self, name):
        try:
            burger = self.burger_service.search_burger(name)
            return jsonify(burger)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def insert_burger(self, data):
        try:
            self.burger_service.insert_burger(data)
            return jsonify({'message': 'Burger added successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def insert_burgers(self, data):
        try:
            if not isinstance(data, list):
                return jsonify({'error': 'Invalid input format, expected a list of burgers.'}), 400

            burgers_added = self.burger_service.insert_burgers(data)
            return jsonify({'message': 'Burgers added successfully', 'burgers': burgers_added}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def update_burger(self, data):
        try:
            self.burger_service.update_burger(data)
            return jsonify({'message': 'Burger updated successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete_burger(self, data):
        try:
            self.burger_service.delete_burger(data)
            return jsonify({'message': 'Burger deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete_all_burgers(self):
        try:
            self.burger_service.delete_all_burgers()
            return jsonify({'message': 'All burgers deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
