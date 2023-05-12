from database.db_connector import SQLite_Connector
from schemas.schemas import Schema
from src.error_message import Error_Message, get_error
from src.success_message import Success_Message


class Todo_Controller(SQLite_Connector):
    def __init__(self) -> None:
        super().__init__()
    
    def get_todos(self, todoId=None) -> dict:

        todos = None
        
        if todoId:
            todos = self.execute_sql_query(f"SELECT * FROM todo WHERE id={todoId}", Schema.todo)
        else:
            todos = self.execute_sql_query(f"SELECT * FROM todo", Schema.todo)

        if todoId and not todos:
            return Schema.api_response(status=200, error_message=[
                Error_Message.todo_not_exist.value])
        elif not todoId and not todos:
            return Schema.api_response(status=200,
                                       error_message=[Error_Message.todo_not_exist.value])
        return Schema.api_response(status=200, data=todos)

    def get_todo_with_userId(self, userId) -> dict:
        todos = self.execute_sql_query(f"SELECT * FROM todo WHERE userId={userId}", Schema.todo)
        
        if len(todos):
            return Schema.api_response(status=400, data=todos)
        else:
            return Schema.api_response(status=400,
                                       error_message=[Error_Message.there_not_existent_todos.value])
        
    def create(self, userId: int, title: str, todo_description: str) -> dict:
        sql_query = f"""
            INSERT INTO todo (
                userId, title, todo_description
            ) VALUES ('{userId}', '{title}', '{todo_description}');"""

        try:
            self.execute_sql_query(sql_query, Schema.todo)
        except Exception as error:
            error_suf = f"{error}".split(".")
            print(error_suf)
            return Schema.api_response(
                status=500,
                error_message=[f"{get_error(error_suf[1])}"]
            )
        todo = self.get_todos()["data"][-1]
        return Schema.api_response(status=200, success_message=[Success_Message.new_todo.value], data=todo)
    
    def update(self, todoId: int, title: str, todo_description: str) -> dict:
        todo = self.get_todos(todoId=todoId)["data"]
        if len(todo):
            sql_query = f"""
                UPDATE todo SET title='{title}', todo_description='{todo_description}'
                WHERE id={todoId}
                """
            try:
                self.execute_sql_query(sql_query, Schema.user)
                return Schema.api_response(
                    status=200,
                    data={"id": todoId, "userId": todo[0]["userId"], "title": title, "todo_description": todo_description},
                    success_message=[Success_Message.todo_updated.value]
                )
            except Exception as error:
                error_suf = f"{error}".split(".")
                return Schema.api_response(
                    status=500,
                    error_message=[f"{get_error(error_suf[1])}"]
                )
        else:
            return Schema.api_response(
                status=404,
                error_message=[Error_Message.todo_not_exist.value]
            )

    def delete(self, todoId: int) -> dict:
        if len(self.get_todos(todoId=todoId)["data"]):
            return Schema.api_response(
                status=200,
                data=self.execute_sql_query(
                    f"""DELETE FROM todo WHERE id={todoId}""", Schema.todo),
                success_message=[Success_Message.deleted_todo.value]
            )
        else:
            return Schema.api_response(
                status=404,
                error_message=[Error_Message.todo_not_exist.value]
            )
        