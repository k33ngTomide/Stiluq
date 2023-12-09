from dataclasses import dataclass


@dataclass
class AddUserRequest:

    def __init__(self):
        email: str
        password: str


