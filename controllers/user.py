from database.db_connector import SQLite_Connector
from schemas.schemas import Schema
from src.error_message import Error_Message, get_error
from src.success_message import Success_Message
import secrets

import random
import bcrypt


class User_Controller(SQLite_Connector):

    def __init__(self) -> None:
        super().__init__()

    def get_user(self, id=None) -> list:

        users = None

        if id:
            users = self.execute_sql_query(
                f"SELECT * FROM user WHERE id={id}", Schema.user)
        else:
            users = self.execute_sql_query(f"SELECT * FROM user", Schema.user)

        if id and not users:
            return Schema.api_response(status=200, error_message=[
                Error_Message.user_not_exist.value])
        elif not id and not users:
            return Schema.api_response(status=200,
                                       error_message=Error_Message.there_not_existent_users.value)
        return Schema.api_response(status=200, data=users)

    def create_new(
            self, first_name: str, last_name: str, email: str, user_password: str, user_type="Stander") -> list:

        # hash_password = bcrypt.hashpw(
        #     user_password.encode("utf-8"), bcrypt.gensalt())

        sql_query = f"""
            INSERT INTO user (
                first_name, last_name, email, hash_password, user_type, account_state
            ) VALUES (
                '{first_name}', '{last_name}', '{email}', '{user_password}', '{user_type}', 1
            );
            """

        try:
            self.execute_sql_query(sql_query, Schema.user)
        except Exception as error:
            error_suf = f"{error}".split(".")
            return Schema.api_response(
                status=500,
                error_message=[f"{get_error(error_suf[1])}"]
            )

        return Schema.api_response(
            status=200,
            data=self.get_user()["data"][-1],
            success_message=[Success_Message.new_user.value]
        )

    def delete_user(self, id: int, admin_password: str) -> bool:
        user = self.get_user(id)["data"][0]
        if admin_password == user["hashPassword"]:
            return Schema.api_response(
                status=200,
                data=self.execute_sql_query(
                    f"""DELETE FROM user WHERE id={id}""", Schema.user),
                success_message=[Success_Message.deleted_user.value]
            )

        return Schema.api_response(
            status=503,
            error_message=[Error_Message.hash_password.value],
        )

    def update_user_password(self, id: int, new_password: str, old_password: str) -> bool:
        user = self.get_user(id)["data"][0]
        if old_password == user["hashPassword"]:
            sql_query = f"""
                UPDATE user SET hash_password='{new_password}'
                WHERE id={id}
                """
            try:
                self.execute_sql_query(sql_query, Schema.user)
                return Schema.api_response(
                    status=200,
                    success_message=[Success_Message.password_updated.value]
                )
            except Exception as error:
                error_suf = f"{error}".split(".")
                return Schema.api_response(
                    status=500,
                    error_message=[f"{get_error(error_suf[1])}"]
                )
        else:
            return Schema.api_response(
                status=200,
                error_message=[Error_Message.hash_password.value]
            )

    def save_access_token(self, id: int, access_token: str) -> None:
        sql_query = f"""
                UPDATE user SET access_token='{access_token}'
                WHERE id={id}
                """
        try:
            self.execute_sql_query(sql_query, Schema.user)
        except:
            pass
                
    def auth_user (self, email: str, password: str) -> list:
        users = self.execute_sql_query(f"SELECT * FROM user WHERE email LIKE '%{email}%'", Schema.user)
        user_exist = len(users) > 0
        if(user_exist and users[0]["hashPassword"] == password):
            access_token = secrets.token_hex(40)
            self.save_access_token(users[0]["id"], access_token)

            return Schema.api_response(
                status=200,
                error_message=[Success_Message.auth_user.value],
                data={"accessToken": access_token, "userName": users[0]["firstName"]}
            )

        else:
            return Schema.api_response(
                status=400,
                error_message=[Error_Message.user_not_exist.value]
            )
    
    def check_access_token(self, accessToken: str) -> None:
        users = self.execute_sql_query(f"SELECT * FROM user WHERE access_token='{accessToken}'", Schema.user)
        user_exist = len(users) > 0
        if(user_exist):
            return Schema.api_response(
                status=200,
                error_message=[Success_Message.valid_access_token.value],
                data={"userName": users[0]["firstName"]}
            )
        else:
            return Schema.api_response(
                status=400,
                error_message=[Error_Message.access_token_not_valid.value]
            )
            