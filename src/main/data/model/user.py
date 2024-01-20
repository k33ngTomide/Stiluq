from flask_login import UserMixin

from validate_email_address import validate_email


class User(UserMixin):
    def __init__(self):
        self.password = None
        self.email = None
        self.username = None
        self.is_logged_in = False
        self.number = None

    def set_login(self, status):
        self.is_logged_in = status

    def get_login(self):
        return self.is_logged_in

    def set_password(self, password):
        self.password = password

    def set_email(self, email):
        if validate_email(email):
            self.email = email

    def get_password(self):
        return self.password

    def get_email(self):
        return self.email
