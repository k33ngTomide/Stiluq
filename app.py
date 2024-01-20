from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, send_file


from data.repository.user_repository_impl import UserRepositoryImpl
from src.main.service.user_service import UserService

app = Flask(__name__)
CORS(app)


user_repository = UserRepositoryImpl()
user_service = UserService(user_repository)


@app.route('/stiluq')
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login_user():
    try:
        request_data = request.get_json()
        login_response = user_service.login(request_data)
        return login_response
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/signup', methods=['POST'])
def register_user():
    try:
        request_data = request.get_json()
        print(request_data)
        register_response = user_service.register(request_data)
        return jsonify(register_response)
    except Exception as e:
        return jsonify({'status': 'error-occurred', 'message': str(e)})


@app.route('/verify', methods=['POST'])
def process_file():
    try:

        uploaded_file = request.files['file']
        user_service.verify_data_in_file(uploaded_file)

        processed_file_path = "src/processed_file.txt"
        return send_file(
            processed_file_path,
            as_attachment=True,
            download_name='processed_file.txt',
            mimetype='text/plain'
        )

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
