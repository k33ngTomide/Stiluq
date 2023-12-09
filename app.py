from flask import Flask, render_template, request
from flask_injector import FlaskInjector
from injector import inject

from src.main.service.user_service import UserService

app = Flask(__name__)


@inject
def configure(binder):
    from data.repository.user_repository import (UserRepository)
    binder.bind(UserRepository, to=UserRepository)
    binder.bind(UserService, to=UserService)


FlaskInjector(app=app, modules=[configure])


@app.route('/stiluq')
def index():
    return render_template("index.html")


@app.route('/start', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    return UserService.verify_data_in_file(file)


if __name__ == '__main__':
    app.run(debug=True)
