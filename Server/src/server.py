import socket
import hashlib      # for hashing passwords
import re           # for checking if nicks and passwords are valid

from Server.src.libs.errors import NameTaken, ValidationException
import Server.src.libs.constants as constants
import Server.src.libs.user_connection

user_data = {}
client_threads = []


def wait_for_connection():  # TODO maciekniewielki add maximum number of connections
    global client_threads
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((constants.SERVER_IP, constants.SERVER_PORT))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        print("Connection from", addr)
        user_thread = Server.src.libs.user_connection.ClientConnection(conn)
        user_thread.run()
        if client_threads:
            client_threads = [x for x in client_threads if x.is_alive()] + [user_thread]
        else:
            client_threads = [user_thread]


def start_server():
    global user_data
    try:
        with open(constants.DATA_FILE, "r") as file:
            for line in file:
                login, hashed_password, highscore = line[:-1].split(" ")
                user_data[login] = (hashed_password, int(highscore))
    except FileNotFoundError:
        open(constants.DATA_FILE, "w").close()
    wait_for_connection()


def _write_user_(user):
    with open(constants.DATA_FILE, "a") as file:
        line = [str(x) for x in user]
        file.write(" ".join(line) + "\n")


def register_user(nick, password):
    global user_data
    if not re.fullmatch(r'[A-Za-z0-9_]+', nick):
        raise ValidationException("BAD_LOGIN")
    if not re.fullmatch(r'[A-Za-z0-9_!@#$%^&]+', password):
        raise ValidationException("BAD_PASSWORD")
    if nick in user_data:
        raise NameTaken("This name is already taken")

    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    user_data[nick] = (hashed_password, 0)
    user = nick, hashed_password, 0
    _write_user_(user)
    print("Registered user", user)
    print(user_data)


def check_password(nick, password):
    global user_data
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    if nick in user_data and user_data[nick][0] == hashed_password:
        return True
    else:
        return False


# TODO maciekniewielki upgrade main loop
def main():
    start_server()


if __name__ == '__main__':
    main()

