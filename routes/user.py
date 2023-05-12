from flask import jsonify
from flask_restful import Resource, reqparse

from controllers.user import User_Controller
from middleware.middleware import Middleware


add_new_args = reqparse.RequestParser()
add_new_args.add_argument("firstName", type=str, required=True, help="Frist name is required.")
add_new_args.add_argument("lastName", type=str, required=True, help="Last name is required.")
add_new_args.add_argument("email", type=str, required=True, help="It is necessary to provide email.")
add_new_args.add_argument("password", type=str, required=True, help="User password is necessary.")

token_args = reqparse.RequestParser()
token_args.add_argument("accessToken", type=str, required=True, help="Access Token is required.")

edit_password_args = reqparse.RequestParser()
edit_password_args.add_argument("oldPassword", type=str, required=True, help="Old Password is required.")
edit_password_args.add_argument("newPassword", type=str, required=True, help="New Password is required.")
edit_password_args.add_argument("accessToken", type=str, required=True, help="Access Token is required.")

user_delete_arg = reqparse.RequestParser()
user_delete_arg.add_argument("password", type=str, required=True, help="User password is required.")
user_delete_arg.add_argument("accessToken", type=str, required=True, help="Access Token is required.")


user_controller = User_Controller()


class Users(Resource):

    def get(self):
        
        args = token_args.parse_args()
        
        next_function = lambda : user_controller.get_user()
        
        result = Middleware.check_user_token(args["accessToken"], next_function)

        return jsonify(result)

    def post(self):

        args = add_new_args.parse_args()

        new_user = user_controller.create_new(
            first_name=args["firstName"],
            last_name=args["lastName"],
            email=args["email"],
            password=args["password"]
        )

        return jsonify(new_user)


class User(Resource):

    def get(self, id):
        
        args = token_args.parse_args()
        
        next_function = lambda : user_controller.get_user(id)
        
        other_next_function = Middleware.check_user_token(args["accessToken"], next_function)
        
        result = Middleware.check_if_user_exist(id, other_next_function)
        
        return jsonify(result)

    def put(self, id):
        args = edit_password_args.parse_args()
        
        next_function = lambda : user_controller.update_user_password(
            id=id, new_password=args["newPassword"], old_password=args["oldPassword"])
        
        other_next_function = Middleware.check_user_token(args["accessToken"], next_function)
        
        result = Middleware.check_if_user_exist(id, other_next_function)

        return jsonify(result)

    def delete(self, id):

        args = user_delete_arg.parse_args()
        
        next_function = lambda : user_controller.delete_user(id, args["password"])
        
        other_next_function = Middleware.check_user_token(args["accessToken"], next_function)
        
        result = Middleware.check_if_user_exist(id, other_next_function)

        return jsonify(result)
