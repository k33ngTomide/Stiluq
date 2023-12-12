import io

from flask import send_file
from injector import inject
from validate_email_address import validate_email

from data.model.user import User
from dtos.response.login_user_response import LoginUserResponse
from dtos.response.logout_user_response import LogoutUserResponse
from exception.UserAlreadyExistsException import UserAlreadyExistsException
from exception.UserNotFoundException import UserNotFoundException
from src.main.service.user_interface import UserInterface
from src.main.dtos.response.add_user_response import AddUserResponse


class UserService(UserInterface):

    @inject
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_user(self, user_id):
        return self.user_repository.find_user(user_id)

    def verify_data_in_file(self, file):
        print("verifying_data_in_file")

        if file.filename == '':
            return "No selected file"

        if file and file.filename.endswith('.txt'):
            processed_file_path = "src/processed_file.txt"

            try:
                with open(processed_file_path, 'w', encoding='utf-8') as file_output:
                    for line in file:
                        email = line.strip().decode('utf-8')
                        print(email)
                        if self.verify_email(email):
                            file_output.write(email + "\n")
            except FileNotFoundError:
                return "File not found", 404

            # file_content = file.read().decode('utf-8')
            # processed_file = io.BytesIO()
            # processed_file.write(f"{email}\n".encode('utf-8'))

    def register(self, add_users_request):

        self.checkIfUserAlreadyExists(add_users_request.email)
        user = User()
        user.set_email(add_users_request.email)
        user.set_password(add_users_request.password)

        saved_user = self.user_repository.save(user)

        add_users_response = AddUserResponse()
        add_users_response._id = saved_user.inserted_id
        add_users_response._message = "Successfully registered user"
        add_users_response._status = "true"

        return add_users_response

    def checkIfUserAlreadyExists(self, email):
        found_user = self.user_repository.find_by_email(email)
        if found_user:
            raise UserAlreadyExistsException("User Already Exists")

    def find_user(self, user_id):
        found_user = self.user_repository.find_user(user_id)
        if found_user:
            return found_user
        else:
            raise UserNotFoundException("User Not Found")

    def login(self, login_request) -> LoginUserResponse:
        user = self.find_user(login_request.id)
        user['is_logged_in'] = True

        self.user_repository.save(user)

        login_response = LoginUserResponse()
        login_response.user_id = user.get('_id')
        login_response.status = user['is_logged_in']
        login_response.message = "Successfully logged in user"
        return login_response

    def logout(self, logout_request):
        user = self.find_user(logout_request.user_id)
        user['is_logged_in'] = True

        self.user_repository.save(user)

        logout_response = LogoutUserResponse()
        logout_response.id = user.get('_id')
        logout_response.status = user['is_logged_in']
        logout_response._message = "Successfully logged out user"
        return logout_response

    def verify_email(self, email):

        if validate_email(email) is True:
            return True
        else:
            return False
