
class Schema:
    
    @staticmethod
    def user(data: tuple) -> list:
        
        return [
            {
                "id": dt[0],
                "firstName": dt[1],
                "lastName": dt[2],
                "email": dt[3],
                "hashPassword": dt[4],
                "userType": dt[5],
                "accountState": dt[6]
            } for dt in data]
    
    @staticmethod
    def api_response(status: int, data=[], success_message=[], error_message=[]) -> list:
        
        return {
            "status": status,
            "successMessage": [{"id": index+1, "message": message} for index, message in enumerate(success_message)],
            "errorMessage": [{"id": index+1, "message": message} for index, message in enumerate(error_message)],
            "data": data
        }
 