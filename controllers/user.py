from database.db_connector import SQLite_Connector
from schemas.schemas import Schema
from src.error_message import Error_Message, get_error
from src.success_message import Success_Message

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
        if admin_password == user["hashPassword"]:
            sql_query = f"""
                UPDATE user SET hash_password='{new_password}'
                WHERE id={id}
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
            success_message=[Success_Message.password_updated.value]
        )
