import socket
import hashlib      # for hashing passwords
import re           # for checking if nicks and passwords are valid

from Server.src.libs.errors import NameTaken, ValidationException

data_file = "user_data.dat"
user_data = []

server_ip = "127.0.0.1"
server_port = 5005
BUFFER_SIZE = 1024


def wait_for_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_ip, server_port))
    s.listen(1)

    conn, addr = s.accept()
    print("Connection from", addr)
    connection(conn)


def connection(conn):       #TODO maciekniewielki finish
    logged_in = 0
    login = ""

    def send_string(s):
        conn.send(s.encode())

    while not logged_in:
        data = conn.recv(BUFFER_SIZE).decode()
        if not data.count(" ") == 2:
            print("Bad data")
            send_string("0 %s" % "Bad data formatting. Do not use spaces in login or password")
            continue
        option, login, password = data.split(" ")
        print("option %s, login %s, password %s", option, login, password)
        if option == "r":
            try:
                register_user(login, password)
            except (ValidationException, NameTaken) as e:
                send_string("0 %s" % e.value)
                continue
            send_string("1 You have been registered and logged in. Your highscore is 0")
            logged_in = 1
        elif option == "l":
            user = [user for user in user_data if user[0] == login]
            if user:
                if check_password(login, password):
                    logged_in = 1
                    print(user)
                    send_string("1 Welcome %s! Your highscore is %s" % (login, user[0][2]))
                else:
                    send_string("0  Wrong password for user %s" % login)
                    continue
            else:
                send_string("0  No user %s in database" % login)
                continue
    print("%s has logged in" % login)
    conn.close()


def start_server():     # TODO maciekniewielki init user connections, open ports
    try:
        with open(data_file, "r") as file:
            for line in file:
                user_data.append(line[:-1].split(" "))
    except FileNotFoundError:
        open(data_file, "w").close()

    wait_for_connection()


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
    print("Registered user", user)


def check_password(nick, password):
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    if len([user for user in user_data if user[1] == hashed_password]):
        return True
    else:
        return False


# TODO maciekniewielki upgrade main loop
def main():
    start_server()


if __name__ == '__main__':
    main()

