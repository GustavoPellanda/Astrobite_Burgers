from flask import Blueprint, request
from server.controllers import BurgerController

class BurgerRoutes:
    def __init__(self):
        self.routes = Blueprint('routes', __name__)
        self.controller = BurgerController()

        self._register_routes()

    def _register_routes(self):
        self.routes.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.routes.add_url_rule('/allBurgers', 'get_all_burgers', self.get_all_burgers, methods=['GET'])
        self.routes.add_url_rule('/topBurgers', 'get_top_burgers', self.get_top_burgers, methods=['GET'])
        self.routes.add_url_rule('/searchBurger', 'search_burger', self.search_burger, methods=['GET'])
        self.routes.add_url_rule('/newBurger', 'insert_burger', self.insert_burger, methods=['POST'])
        self.routes.add_url_rule('/newBurgers', 'insert_burgers', self.insert_burgers, methods=['POST'])
        self.routes.add_url_rule('/updateBurger', 'update_burger', self.update_burger, methods=['PUT'])
        self.routes.add_url_rule('/deleteBurger', 'delete_burger', self.delete_burger, methods=['DELETE'])
        self.routes.add_url_rule('/deleteAllBurgers', 'delete_all_burgers', self.delete_all_burgers, methods=['DELETE'])

    def index(self):
        return 'Astrobite Burgers server up!'

    def get_all_burgers(self):
        return self.controller.get_all_burgers()

    def get_top_burgers(self):
        return self.controller.get_top_burgers()

    def search_burger(self):
        name = request.args.get('name')
        return self.controller.search_burger(name)

    def insert_burger(self):
        data = request.json
        return self.controller.insert_burger(data)

    def insert_burgers(self):
        data = request.json
        return self.controller.insert_burgers(data)

    def update_burger(self):
        data = request.json
        return self.controller.update_burger(data)

    def delete_burger(self):
        data = request.json
        return self.controller.delete_burger(data)

    def delete_all_burgers(self):
        return self.controller.delete_all_burgers()
