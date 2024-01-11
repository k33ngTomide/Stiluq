import io

from flask import Flask, render_template, request, jsonify, send_file
from validate_email_address import validate_email

from data.repository.user_repository_impl import UserRepositoryImpl
from src.main.service.user_service import UserService

app = Flask(__name__)

user_repository = UserRepositoryImpl()
instance = UserService(user_repository)


@app.route('/stiluq')
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login_user():
    try:
        request_data = request.get_json()
        login_response = instance.login(request_data)
        return login_response
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/signup')
def register_user():
    try:
        request_data = request.get_json()
        register_response = instance.register(request_data)
        return register_response
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/verify', methods=['POST'])
def process_file():
    try:

        uploaded_file = request.files['file']
        instance.verify_data_in_file(uploaded_file)

        processed_file_path = "src/processed_file.txt"
        return send_file(
            processed_file_path,
            as_attachment=True,
            download_name='processed_file.txt',
            mimetype='text/plain'
        )

        # processed_file = io.BytesIO()
        # for line in uploaded_file:
        #     email = line.strip().decode('utf-8')
        #     print(email)
        #
        #     if validate_email(email):
        #         processed_file.write(f"{email}\n".encode('utf-8'))

        # return jsonify({'processed_file': processed_file.read().decode('utf-8')})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
