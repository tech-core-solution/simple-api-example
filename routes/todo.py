from flask import jsonify
from flask_restful import Resource, reqparse

from middleware.middleware import Middleware
from controllers.todo import Todo_Controller


add_new_args = reqparse.RequestParser()
add_new_args.add_argument("userId", type=str, required=True, help="User ID is required.")
add_new_args.add_argument("title", type=str, required=True, help="Title is required.")
add_new_args.add_argument("todoDescription", type=str, required=True, help="Todo Description is required.")
add_new_args.add_argument("accessToken", type=str, required=True, help="Access Token is required.")

get_args  = reqparse.RequestParser()
get_args.add_argument("userId", type=str, required=True, help="User ID is required.")
get_args.add_argument("accessToken", type=str, required=True, help="Access Token is required.")

token_args = reqparse.RequestParser()
token_args.add_argument("accessToken", type=str, required=True, help="Access Token is required.")

edit_args = reqparse.RequestParser()
edit_args.add_argument("title", type=str, required=True, help="Title is required.")
edit_args.add_argument("todoDescription", type=str, required=True, help="Todo Description is required.")
edit_args.add_argument("accessToken", type=str, required=True, help="Access Token is required.")


todo_controller = Todo_Controller()


class Todos(Resource):

    def get(self):

        args = get_args.parse_args()

        next_function = lambda : todo_controller.get_todo_with_userId(args["userId"])
        
        other_next_function = lambda : Middleware.check_user_token(args["accessToken"], next_function)
        
        result = Middleware.check_if_user_exist(args["userId"], other_next_function)

        return jsonify(result)

    def post(self):

        args = add_new_args.parse_args()

        next_function = lambda : todo_controller.create(
            args["userId"], args["title"], args["todoDescription"])
        
        other_next_function = lambda : Middleware.check_user_token(
            args["accessToken"], next_function)
        
        response = Middleware.check_if_user_exist(args["userId"], other_next_function)
        
        return jsonify(response)


class Todo(Resource):

    def get(self, id):

        args = token_args.parse_args()

        next_function = lambda : todo_controller.get_todos(id)
        
        other_next_function = lambda : Middleware.check_user_token(args["accessToken"], next_function)

        result = Middleware.check_user_token(id, other_next_function)
        
        return jsonify(result)

    def put(self, id):

        args = edit_args.parse_args()

        next_function = lambda : todo_controller.update(id, args["title"], args["todoDescription"])
        
        other_next_function = lambda : Middleware.check_user_token(args["accessToken"], next_function)
        
        result = Middleware.check_user_token(id, other_next_function)

        return jsonify(result)

    def delete(self, id):

        args = token_args.parse_args()

        next_function = lambda : todo_controller.delete(id)
        
        other_next_function = lambda : Middleware.check_user_token(args["accessToken"], next_function)
        
        result = Middleware.check_user_token(id, other_next_function)

        return jsonify(result)
