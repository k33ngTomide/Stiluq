import io

from flask import send_file
from injector import inject
from validate_email_address import validate_email

from data.model.user import User
from exception.UserAlreadyExistsException import UserAlreadyExistsException
from src.main.dtos.response.add_user_response import AddUserResponse


class UserService:

    @inject
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_user(self, user_id):
        return self.user_repository.find_user(user_id)

    @staticmethod
    def verify_data_in_file(file):

        if file.filename == '':
            return "No selected file"

        if file and file.filename.endswith('.txt'):

            file_content = file.read().decode('utf-8')
            processed_file = io.BytesIO()

            for line in file_content.split("\n"):
                email = line.strip()
                print(email)

                if validate_email(email):
                    print(email)
                    processed_file.write(f"{email}\n".encode('utf-8'))

            current_file = processed_file

            return send_file(
                processed_file,
                as_attachment=True,
                download_name='processed_file.txt',
                mimetype='text/plain'
            )

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

