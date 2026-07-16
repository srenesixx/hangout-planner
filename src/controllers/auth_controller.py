import src.models.auth as auth_model

class AuthController:
    """Controller to handle user authentication, registration, password change, and balance updates."""
    
    @staticmethod
    def register_user(nama: str, username: str, email: str, password: str, initial_saldo: int = 0) -> tuple[bool, str]:
        return auth_model.register_user(nama, username, email, password, initial_saldo)

    @staticmethod
    def login_user(username_or_email: str, password: str) -> dict | None:
        return auth_model.login_user(username_or_email, password)

    @staticmethod
    def get_user_by_id(user_id: int) -> dict | None:
        return auth_model.get_user_by_id(user_id)

    @staticmethod
    def update_saldo(user_id: int, new_saldo: int) -> bool:
        return auth_model.update_saldo(user_id, new_saldo)

    @staticmethod
    def change_password(user_id: int, current_password: str, new_password: str) -> tuple[bool, str]:
        return auth_model.change_password(user_id, current_password, new_password)
