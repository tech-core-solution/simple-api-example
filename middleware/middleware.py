from controllers.user import User_Controller
from src.error_message import Error_Message
from schemas.schemas import Schema


class Middleware():

    user_controller = User_Controller()

    @staticmethod
    def check_user_token(accessToken: str, nextFunction) -> dict:
        user = Middleware.user_controller.check_access_token(accessToken)

        if (user["status"] == 200):
            return nextFunction()

        return Schema.api_response(
            status=400,
            error_message=[Error_Message.access_token_not_valid.value]
        )
    
    @staticmethod
    def check_if_user_exist(id: int, nextFunction) -> dict:
        user = Middleware.user_controller.get_user(id)["data"]

        if (len(user)):
            return nextFunction()

        return Schema.api_response(
            status=400,
            error_message=[Error_Message.user_not_exist.value]
        )
