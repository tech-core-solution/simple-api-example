from enum import Enum

class Error_Message(Enum):
    
    id_not_exist = "This user ID doesn't exist"
    user_not_exist = "This user doesn't exist"
    todo_not_exist = "This todo doesn't exist"
    there_not_existent_users = "There is no registered users on this app"
    there_not_existent_todos = "There is no registered todos for this user"
    email_already_exist = "This email address is already in use"
    equal_password = "Old and New password are the both the same"
    hash_password = "Wrong user password"
    internal_error = "Server internal Error"
    access_token_not_valid = "Access Token is not valid"


def get_error(error_suf: str) -> str:
    return [
        error_message.value for error_name, error_message in Error_Message.__members__.items() 
            if error_name == f"{error_suf}_already_exist"
    ][0]
