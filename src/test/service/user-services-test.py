import unittest

from injector import inject

from data.repository.user_repository import UserRepository
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
        print(add_users_response._id)
        self.assertIsNotNone(add_users_response)

    def test_that_user_registration_isUnique(self):
        add_users_request = add_user_request.AddUserRequest()
        add_users_request.email = "muiliyu@gmail.com"
        add_users_request.password = "<PASSWORD>"

        add_users_response = self.instance.register(add_users_request)
        print(add_users_response._id)
        self.assertIsNotNone(add_users_response)

        add_users_request1 = add_user_request.AddUserRequest()
        add_users_request1.email = "muiliyu@gmail.com"
        add_users_request1.password = "<PASSWORD>"

        self.assertRaises(UserAlreadyExistsException, self.instance.register, add_users_request1)


if __name__ == '__main__':
    unittest.main()
