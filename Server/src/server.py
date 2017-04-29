import socket
import hashlib      #for hashing passwords
import re           #for checking if nicks and passwords are valid

from Server.src.libs.errors import NameTaken, ValidationException

data_file = "user_data.dat"
user_data = []


def start_server():
    try:
        with open(data_file, "r") as file:
            for line in file:
                user_data.append(line.split(" "))
    except FileNotFoundError:
        open(data_file, "w").close()


def _write_user_(user):
    with open(data_file, "a") as file:
        line = [str(x) for x in user]
        file.write(" ".join(line) + "\n")


def register_user(nick, password):
    if not re.fullmatch(r'[A-Za-z0-9_]+', nick):
        raise ValidationException("BAD_LOGIN")
    if not re.fullmatch(r'[A-Za-z0-9_!@#$%^&]+', password):
        raise ValidationException("BAD_PASSWORD")
    if any(x[0] == nick for x in user_data):
        raise NameTaken("This name is already taken")

    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    user = nick, hashed_password, 0
    user_data.append(user)
    _write_user_(user)


