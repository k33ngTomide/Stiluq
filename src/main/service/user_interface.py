from abc import ABC


class UserInterface(ABC):

    def get_user(self, user_id):
        pass

    def verify_email(self, email):
        pass

    def find_user(self, user_id):
        pass

    def login(self, login_user_request):
        pass

    def logout(self, logout_user_request):
        pass

    def register(self, register_user_request):
        pass
