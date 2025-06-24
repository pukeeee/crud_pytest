class UserRepository:
    def create_user(self, user: dict) -> dict:
        raise NotImplementedError

    def get_user_by_email(self, email: str) -> dict:
        raise NotImplementedError