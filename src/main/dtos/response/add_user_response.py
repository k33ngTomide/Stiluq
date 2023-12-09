from dataclasses import dataclass


@dataclass
class AddUserResponse:
    def __init__(self):
        self._id = str
        self._message = str
        self._status = str
