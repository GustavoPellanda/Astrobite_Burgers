from flask import Flask
from server.routes import BurgerRoutes

def create_app():
    app = Flask(__name__)
    burger_routes = BurgerRoutes()
    app.register_blueprint(burger_routes.routes)
    return app
