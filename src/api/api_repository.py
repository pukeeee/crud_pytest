class UserRepository:
    def create_user(self, user: dict) -> dict:
        raise NotImplementedError

    def get_user_by_email(self, email: str) -> dict:
        raise NotImplementedError
    
    def get_user_by_id(self, id: str) -> dict:
        raise NotImplementedError
    
    def update_user(self, id: int, user: dict) -> dict:
        raise NotImplementedError
    
    def update_password(self, id: int, password: str) -> dict:
        raise NotImplementedError