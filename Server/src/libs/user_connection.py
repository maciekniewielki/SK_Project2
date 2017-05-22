import socket
import threading
import Server.src.libs.constants as constants
import Server.src.server as server
from Server.src.libs.errors import NameTaken, ValidationException


class ClientConnection(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def send_string(self, s):
        self.connection.send(s.encode())

    def run(self):       # TODO maciekniewielki finish
        logged_in = 0
        login = ""

        while not logged_in:
            data = self.connection.recv(constants.BUFFER_SIZE).decode()
            if not data.count(" ") == 2:
                print("Bad data")
                self.send_string("0 %s" % "Bad data formatting. Do not use spaces in login or password")
                continue
            option, login, password = data.split(" ")
            print("option %s, login %s, password %s" % (option, login, password))
            if option == "r":
                try:
                    with ClientConnection.lock:
                        server.register_user(login, password)

                except (ValidationException, NameTaken) as e:
                    self.send_string("0 %s" % e.value)
                    continue
                self.send_string("1 You have been registered and logged in. Your highscore is 0")
                logged_in = 1
            elif option == "l":
                print(server.user_data)
                if login in server.user_data:
                    with ClientConnection.lock:
                        result = server.check_password(login, password)
                    if result:
                        logged_in = 1
                        self.send_string("1 Welcome %s! Your highscore is %s" % (login, server.user_data[login][1]))
                    else:
                        self.send_string("0  Wrong password for user %s" % login)
                        continue
                else:
                    self.send_string("0  No user %s in database" % login)
                    continue
        print("%s has logged in" % login)
        self.connection.close()
