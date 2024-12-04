from database.database import Database

class BurgerService:
    def __init__(self):
        self.database = Database()

    def get_all_burgers(self):
        return self.database.get_all_burgers()

    def get_top_burgers(self):
        return self.database.get_top_burgers()

    def search_burger(self, name):
        return self.database.search_burger(name)

    def insert_burger(self, data):
        self.database.insert_burger(data['name'], data['price'], data['ingredients'])

    def insert_burgers(self, data):
        burgers_added = []
        for burger in data:
            self.database.insert_burger(burger['name'], burger['price'], burger['ingredients'])
            burgers_added.append({
                "name": burger['name'],
                "price": burger['price'],
                "ingredients": burger['ingredients']
            })
        return burgers_added

    def update_burger(self, data):
        self.database.update_burger(data['id'], data['name'], data['price'], data['ingredients'])

    def delete_burger(self, data):
        self.database.delete_burger(data['id'])
        self.database.update_burger_ids()

    def delete_all_burgers(self):
        self.database.delete_all_burgers()
