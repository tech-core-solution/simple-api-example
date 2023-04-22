from enum import Enum

class Success_Message(Enum):
    
    new_user = "User created successfully"
    password_updated = "Password updated successfully"
    deleted_user = "User deleted successfully",
    auth_user = "User logged in successfully"
    valid_access_token = "The access Token is valid"
    