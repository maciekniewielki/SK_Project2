import socket
import hashlib      # for hashing passwords
import re           # for checking if nicks and passwords are valid

from Server.src.libs.errors import NameTaken, ValidationException
import Server.src.libs.constants as constants
import Server.src.libs.user_connection
import random


class GameServer:                   # TODO maciekniewielki add port and data file in constructor

    def __init__(self):
        self.user_data = {}
        self.client_threads = []
        self.word_list = []

    def load_user_data(self):
        try:
            with open(constants.DATA_FILE, "r") as file:
                for line in file:
                    login, hashed_password, highscore = line[:-1].split(" ")
                    self.user_data[login] = (hashed_password, int(highscore))
        except FileNotFoundError:
            open(constants.DATA_FILE, "w").close()

    def load_word_list(self):
        try:
            with open(constants.WORDS_FILE, "r") as file:
                for line in file:
                    self.word_list.append(line[:-1])
        except FileNotFoundError:
            open(constants.WORDS_FILE, "w").close()

    def wait_for_connection(self):  # TODO maciekniewielki add maximum number of connections
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((constants.SERVER_IP, constants.SERVER_PORT))
        s.listen(1)

        while True:
            conn, addr = s.accept()
            print("Connection from", addr)
            user_thread = Server.src.libs.user_connection.ClientConnection(self, conn, addr)
            user_thread.start()
            if self.client_threads:
                self.client_threads = [x for x in self.client_threads if x.is_alive()] + [user_thread]
            else:
                self.client_threads = [user_thread]

    def start_server(self):
        self.load_user_data()
        self.load_word_list()
        self.wait_for_connection()

    def _write_user_(self, user):
        with open(constants.DATA_FILE, "a") as file:
            line = [str(x) for x in user]
            file.write(" ".join(line) + "\n")

    def register_user(self, nick, password):
        if not re.fullmatch(r'[A-Za-z0-9_]+', nick):
            raise ValidationException("Bad login format. You can only use letters, numbers and underscores")
        if not re.fullmatch(r'[A-Za-z0-9_!@#$%^&]+', password):
            raise ValidationException("Bad password format. You can only use letters, numbers and _!@#$%^&")
        if nick in self.user_data:
            raise NameTaken("This name is already taken")

        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        self.user_data[nick] = (hashed_password, 0)
        user = nick, hashed_password, 0
        self._write_user_(user)
        print("Registered user", user[0])

    def check_password(self, nick, password):
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        if nick in self.user_data and self.user_data[nick][0] == hashed_password:
            return True
        else:
            return False

    def get_highscore(self, login):
        return self.user_data[login][1]

    def exits_user(self, nick):
        return nick in self.user_data

    def get_random_words(self, quantity=60):
        words = [random.choice(self.word_list) for _ in range(quantity)]
        return words


def main():
    game = GameServer()
    game.start_server()


if __name__ == '__main__':
    main()

