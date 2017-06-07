import hashlib  # for hashing passwords
import random
import re  # for checking if logins and passwords are valid
import socket

from resources.errors import NameTaken, ValidationException

import user_connection
import localizer
import resources.constants as constants


class GameServer:
    """Base class for the server"""

    def __init__(self):
        self.user_data = {}
        self.client_threads = []
        self.word_list = []
        self.best_highscores = []
        self.versus_queue = []

    def refresh_client_threads(self):
        """Removes dead threads from the thread list"""
        self.client_threads = [x for x in self.client_threads if x.is_alive()]

    def load_user_data(self):
        """Loads user database(logins, hashes and highscores) from file"""
        try:
            with open(constants.DATA_FILE, "r") as file:
                    for line in file:
                        login, hashed_password, highscore = line[:-1].split(" ")
                        self.user_data[login] = (hashed_password, int(highscore))
        except FileNotFoundError:
            open(constants.DATA_FILE, "w").close()

    def load_word_list(self):
        """Loads the lists of words from file to memory"""
        print("Loading word list")
        try:
            with open(constants.WORDS_FILE, "r") as file:
                for line in file:
                    self.word_list.append(line[:-1])
        except FileNotFoundError:
            open(constants.WORDS_FILE, "w").close()

    def wait_for_connection(self):
        """Creates a TCP socket on port taken from constants.py and listens for connections.
        If someone connects, a child thread is created and the connection socket is assigned to it.
        Also keeps track of the number of open connections.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", constants.SERVER_PORT))
        s.listen(1)
        print("Waiting for clients")
        while True:
            conn, addr = s.accept()
            self.refresh_client_threads()
            print("Connection from", addr)
            if len(self.client_threads) >= constants.MAX_CONNECTIONS:
                conn.close()
                print("Too many connections, couldn't connect %s" % (addr,))
                continue

            user_thread = user_connection.ClientConnection(self, conn, addr)
            user_thread.start()
            self.client_threads.append(user_thread)
            print("Current clients: %d" % len(self.client_threads))

    def start_server(self):
        """Loads every resource that is needed for the proper work. Then starts waiting for connections
        Also starts the Localizer service.
        """
        print("Starting server")
        self.load_user_data()
        self.load_word_list()
        self.update_best_highscores()
        localizer.Localizer().start()
        self.wait_for_connection()

    def _write_user_(self, user):
        """Appends user data to database file"""
        with open(constants.DATA_FILE, "a") as file:
            line = [str(x) for x in user]
            file.write(" ".join(line) + "\n")

    def register_user(self, login, password):
        """Checks if login and password are valid and then registers the user"""
        if not re.fullmatch(r'[A-Za-z0-9_]{1,30}', login):
            raise ValidationException("Bad login format. You can only use letters, numbers and underscores(1-30 chars)")
        if not re.fullmatch(r'[A-Za-z0-9_!@#$%^&]{1,30}', password):
            raise ValidationException("Bad password format. You can only use letters, numbers and _!@#$%^& (1-30 chars)")
        if login in self.user_data:
            raise NameTaken("This name is already taken")

        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        self.user_data[login] = (hashed_password, 0)
        user = login, hashed_password, 0
        self._write_user_(user)
        self.update_best_highscores()
        print("Registered user", user[0])

    def check_password(self, login, password):
        """Checks if the supplied password matches with database"""
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        if login in self.user_data and self.user_data[login][0] == hashed_password:
            return True
        else:
            return False

    def get_highscore(self, login):
        """Returns highscore for the given login"""
        return self.user_data[login][1]

    def exits_user(self, login):
        """Checks if there is already a user registered in the database"""
        return login in self.user_data

    def get_random_words(self, quantity=60):
        """Returns a list with random words from the word database"""
        words = [random.choice(self.word_list) for _ in range(quantity)]
        return words

    def save_user_data(self):
        """Dumps the user database from memory to file"""
        with open(constants.DATA_FILE, "w") as file:
            for login, data in self.user_data.items():
                line = "%s %s %d\n" % (login, data[0], data[1])
                file.write(line)

    def update_highscore(self, login, highscore):
        """Updates the highscore both in memory and in database file"""
        self.user_data[login] = (self.user_data[login][0], highscore)
        self.save_user_data()
        self.update_best_highscores()

    def update_best_highscores(self):
        """Sorts the list of highscores on the server to get the best 5 and updates them"""
        all_highscores = []
        for login, data in self.user_data.items():
            all_highscores.append((login, data[1]))
        all_highscores.sort(key=lambda x: x[1], reverse=True)
        self.best_highscores = all_highscores[:5]

    def get_best_highscores_string(self):
        """Returns a formatted string of best highscores"""
        places = []
        for index, player in enumerate(self.best_highscores):
            line = "%d. %s %d" % (index+1, player[0], player[1])
            places.append(line)
        if not places:
            return "There are no current highscores"
        return "\n".join(places)

    def add_to_versus_queue(self, client):
        """Adds a client to the waiting queue and if there is already someone else, matches them with each other"""
        self.versus_queue.append(client)
        print("%s is waiting for a versus match" % client.login)
        if len(self.versus_queue) != 2:
            return
        word_list = self.get_random_words()
        player_1 = self.versus_queue.pop()
        player_2 = self.versus_queue.pop()
        player_1.prepare_for_versus(word_list[:], player_2.login, player_2.my_versus_score)
        player_2.prepare_for_versus(word_list[:], player_1.login, player_1.my_versus_score)


def main():
    game = GameServer()
    game.start_server()


if __name__ == '__main__':
    main()

