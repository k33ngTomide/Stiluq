import bcrypt
from injector import inject
from validate_email_address import validate_email

from data.model.user import User
from exception.UserAlreadyExistsException import UserAlreadyExistsException
from exception.UserNotFoundException import UserNotFoundException
from src.main.service.user_interface import UserInterface


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

    def register(self, add_users_request):
        self.checkIfUserAlreadyExists(add_users_request.get('email'))
        user = User()
        user.username = add_users_request.get('username')
        user.set_email(add_users_request.get('email'))
        user.number = add_users_request.get('number')

        raw_password = add_users_request.get('password')
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        user.set_password(hashed_password.decode('utf-8'))

        saved_user = self.user_repository.save(user)
        new_id = str(saved_user.inserted_id)

        return {
            'user_id': new_id,
            'message': "Successfully registered user",
            'status': 'ok'
        }

    def checkIfUserAlreadyExists(self, email):
        found_user = self.user_repository.find_by_email(email)
        if found_user:
            raise UserAlreadyExistsException("User Already Exists")

    def find_user(self, user_email):
        found_user = self.user_repository.find_by_email(user_email)
        if found_user:
            return found_user
        else:
            raise UserNotFoundException("User Not Found")

    def login(self, login_request):
        user = self.find_user(login_request.get('email'))
        hashed_login_password = bcrypt.hashpw(login_request.get('password').encode('utf-8'), bcrypt.gensalt())
        if bcrypt.checkpw(hashed_login_password, user.get_password()):
            user['is_logged_in'] = True
            updated_user = self.user_repository.save(user)
            return {
                'user': str(updated_user),
                'message': "Successfully logged in user",
                'status': 'ok'
            }
        else:
            return {
                'message': "Invalid Credentials, username or password incorrect",
                'status': 'failed'
            }

    def logout(self, logout_request):
        user = self.find_user(logout_request.user_id)
        user['is_logged_in'] = True

        updated_user = self.user_repository.save(user)
        return {
            'user_id': updated_user.get('_id'),
            'message': "Successfully logged out user",
            'status': 'ok'
        }

    def verify_email(self, email):

        if validate_email(email) is True:
            return True
        else:
            return False
