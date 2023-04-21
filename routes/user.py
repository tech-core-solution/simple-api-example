from flask import jsonify
from flask_restful import Api, Resource, reqparse


from controllers.user import User_Controller


add_new_args = reqparse.RequestParser()
add_new_args.add_argument("firstName", type=str,
                          required=True, help="Frist name is required.")
add_new_args.add_argument("lastName", type=str,
                          required=True, help="Last name is required.")
add_new_args.add_argument("email", type=str, required=True,
                          help="It is necessary to provide email.")
add_new_args.add_argument("userPassword", type=str,
                          required=True, help="User password is necessary.")

edit_password_args = reqparse.RequestParser()
edit_password_args.add_argument(
    "oldPassword", type=str, required=True, help="Old Password is required.")
edit_password_args.add_argument(
    "newPassword", type=str, required=True, help="New Password is required.")

user_delete_arg = reqparse.RequestParser()
user_delete_arg.add_argument(
    "password", type=str, required=True, help="User password is required.")


user_controller = User_Controller()


class Users(Resource):

    def get(self):

        return jsonify(user_controller.get_user())

    def post(self):

        args = add_new_args.parse_args()

        new_user = user_controller.create_new(
            first_name=args["firstName"],
            last_name=args["lastName"],
            email=args["email"],
            user_password=args["userPassword"]
        )

        return jsonify(new_user)


class User(Resource):

    def get(self, id):
        return jsonify(user_controller.get_user(id))

    def put(self, id):
        args = edit_password_args.parse_args()

        return jsonify(user_controller.update_user_password(id, args["newPassword"]), args["oldPassword"])

    def delete(self, id):

        args = user_delete_arg.parse_args()
        return jsonify(user_controller.delete_user(id, args["password"]))
