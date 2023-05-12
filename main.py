from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource

from routes.user import User, Users
from routes.todo import Todo, Todos
from routes.auth import Auth_User


app = Flask(__name__)

CORS(app, supports_credentials=True)
api = Api(app)

class Simple_User_API(Resource):

    def get(self):
        return "Simple user API"


class Bank_Simulator_Restfull_API():
    @staticmethod
    def start():
        api.add_resource(Simple_User_API, "/")
        api.add_resource(Users, "/users")
        api.add_resource(User, "/user/<int:id>")
        api.add_resource(Todos, "/todos")
        api.add_resource(Todo, "/todo/<id>")
        api.add_resource(Auth_User, "/sign-in")
        app.run(debug=True)


if __name__ == "__main__":

    Bank_Simulator_Restfull_API.start()
