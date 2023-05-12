from enum import Enum

class Success_Message(Enum):
    
    new_user = "User created successfully"
    new_todo = "Todo created successfully"
    password_updated = "Password updated successfully"
    todo_updated = "Todo updated successfully"
    deleted_user = "User deleted successfully",
    deleted_todo = "Todo deleted successfully",
    auth_user = "User logged in successfully"
    valid_access_token = "The access Token is valid"
    