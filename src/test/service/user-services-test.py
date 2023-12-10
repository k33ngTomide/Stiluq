import unittest

from injector import inject

from data.repository.user_repository import UserRepository
from dtos.request import login_user_request
from dtos.request.logout_user_request import LogoutRequest
from exception.UserAlreadyExistsException import UserAlreadyExistsException
from src.main.dtos.request import add_user_request
from src.main.dtos.response import add_user_response
from src.main.service.user_service import UserService


class MyTestCase(unittest.TestCase):

    @inject
    def setUp(self):
        user_repo = UserRepository()
        user_repo.delete_all()
        self.instance = UserService(user_repo)

    def test_that_user_can_register(self):
        add_users_request = add_user_request.AddUserRequest()
        add_users_request.email = "muiliyu@gmail.com"
        add_users_request.password = "<PASSWORD>"

        add_users_response = self.instance.register(add_users_request)
        self.assertIsNotNone(add_users_response)

    def test_that_user_registration_isUnique(self):
        add_users_request = add_user_request.AddUserRequest()
        add_users_request.email = "muiliyu@gmail.com"
        add_users_request.password = "<PASSWORD>"

        add_users_response = self.instance.register(add_users_request)
        self.assertIsNotNone(add_users_response)

        add_users_request1 = add_user_request.AddUserRequest()
        add_users_request1.email = "muiliyu@gmail.com"
        add_users_request1.password = "<PASSWORD>"

        self.assertRaises(UserAlreadyExistsException, self.instance.register, add_users_request1)

    def test_that_user_can_login(self):
        add_users_request = add_user_request.AddUserRequest()
        add_users_request.email = "muiliyu@gmail.com"
        add_users_request.password = "<PASSWORD>"

        add_users_response = self.instance.register(add_users_request)
        self.assertIsNotNone(add_users_response)

        login_request = login_user_request.LoginUserRequest()
        login_request.id = add_users_response._id

        login_response = self.instance.login(login_request)
        self.assertIsNotNone(login_response)

    def test_that_user_can_logout(self):
        add_users_request = add_user_request.AddUserRequest()
        add_users_request.email = "muiliyu@gmail.com"
        add_users_request.password = "<PASSWORD>"

        add_users_response = self.instance.register(add_users_request)
        self.assertIsNotNone(add_users_response)

        login_request = login_user_request.LoginUserRequest()
        login_request.id = add_users_response._id

        login_response = self.instance.login(login_request)
        self.assertIsNotNone(login_response)

        logout_request = LogoutRequest()
        logout_request.user_id = add_users_response._id
        logout_response = self.instance.logout(logout_request)
        self.assertIsNotNone(logout_response)


if __name__ == '__main__':
    unittest.main()
