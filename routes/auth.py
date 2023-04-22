from flask import jsonify
from flask_restful import Api, Resource, reqparse


from controllers.user import User_Controller


auth_user_args = reqparse.RequestParser()
auth_user_args.add_argument(
    "email", type=str, required=False, default=None, help="Email is required.")
auth_user_args.add_argument(
    "password", type=str, required=False, default=None, help="Password is required.")
auth_user_args.add_argument(
    "accessToken", type=str, required=False, default=None, help="Password is required.")


user_controller = User_Controller()


class Auth_User(Resource):

    def post(self):

        args = auth_user_args.parse_args()

        if args["accessToken"]:
            return user_controller.check_access_token(accessToken=args["accessToken"])
        
        return user_controller.auth_user(
            email=args["email"],
            password=args["password"]
        )
