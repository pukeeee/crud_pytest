class UserRepository:
    def create_suer(self, user: dict) -> dict:
        raise NotImplementedError
    
    def get_user(self, user_id: str) -> dict:
        raise NotImplementedError