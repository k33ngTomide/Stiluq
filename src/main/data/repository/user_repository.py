from abc import ABC

from data.model.user import User


class UserRepository(ABC):

    def save(self, user):
        pass

    def find_user(self, user_id):
        pass

    def find_by_email(self, email_address):
        pass

    def delete_all(self):
        pass

