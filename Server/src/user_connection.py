import threading

from resources.errors import NameTaken, ValidationException

import resources.constants as constants
from time import time


class ClientConnection(threading.Thread):
    """Base class for handling the client connection"""
    lock = threading.Lock()

    def __init__(self, game_server, connection, address):
        super().__init__()
        self.game_server = game_server
        self.connection = connection
        self.address = address
        self.login = ""
        self.versus_words = []
        self.other_login = ""
        self.versus_start = False
        self.other_versus_score = [0]
        self.my_versus_score = [0]
        self.versus_start_time = 0

    def receive_data(self):
        """Tries to receive data from client. If the Connection is closed returns None"""
        try:
            data = self.connection.recv(constants.BUFFER_SIZE).decode()
        except ConnectionAbortedError:
            print("User %s has disconnected" % (self.address,))
            self.connection.close()
            return None
        return data

    def send_string(self, s):
        """Sends a string to the client"""
        self.connection.send(s.encode())

    def try_login(self, login, password):
        """Tries to log in the user with supplied data. Returns true on success and False otherwise"""
        with ClientConnection.lock:
            exists = self.game_server.exits_user(login)
        if exists:
            with ClientConnection.lock:
                result = self.game_server.check_password(login, password)
            if result:
                return True
            else:
                self.send_string("0  Wrong password for user %s" % login)
        else:
            self.send_string("0  No user %s in database" % login)
        return False

    def try_register(self, login, password):
        """Tries to register the user with supplied data. Returns true on success and False otherwise"""
        try:
            with ClientConnection.lock:
                self.game_server.register_user(login, password)
        except (ValidationException, NameTaken) as e:
            self.send_string("0 %s" % e.value)
            return False
        return True

    def accept_connection(self):
        """Handles the server side of login menu"""
        logged_in = False

        while not logged_in:
            data = self.receive_data()
            if data is None:
                return None

            if not data.count(" ") == 2:
                self.send_string("0 %s" % "Bad data formatting. Do not use spaces in login or password")
                continue
            option, login, password = data.split(" ")

            if option == "r":
                logged_in = self.try_register(login, password)
            elif option == "l":
                logged_in = self.try_login(login, password)
        return login

    def single_player(self):
        """Handles the singleplayer game using a send-receive-check loop. Returns player score."""
        with ClientConnection.lock:
            words = self.game_server.get_random_words()

        game_ended = False
        score = 0

        current_word = words.pop()
        self.send_string(current_word)
        while not game_ended:
            correct = False
            while not correct:
                typed_word = self.receive_data()
                if typed_word is None:
                    return None
                elif typed_word == "#":
                    return score
                elif typed_word == current_word:
                    score += len(current_word)
                    correct = True
                else:
                    self.send_string(current_word)
            current_word = words.pop()
            self.send_string(current_word)

    def prepare_for_versus(self, words, other_login, other_versus_score):
        """Sets the metadata about the versus opponent and the word list. Then sets a start flag"""
        self.versus_words = words
        self.other_login = other_login
        self.other_versus_score = other_versus_score
        self.versus_start_time = time()
        self.versus_start = True

    def versus(self):
        """Handles the versus game. Similar to singleplayer"""
        game_ended = False
        self.my_versus_score[0] = 0
        self.send_string(self.other_login)
        current_word = self.versus_words.pop()
        current_time = int(time() - self.versus_start_time)
        self.send_string("%s %d %d %d" % (current_word, self.my_versus_score[0], self.other_versus_score[0], 0))
        while not game_ended:
            correct = False
            while not correct:
                typed_word = self.receive_data()
                current_time = int(time() - self.versus_start_time)
                if current_time > 60:
                    self.my_versus_score.append(0)
                    while len(self.other_versus_score) < 2:
                        pass
                    return self.my_versus_score[0], self.other_versus_score[0]
                elif typed_word is None:
                    return None
                elif typed_word == current_word:
                    self.my_versus_score[0] += len(current_word)
                    correct = True
                else:
                    self.send_string("%s %d %d %d" % (current_word, self.my_versus_score[0], self.other_versus_score[0], current_time))
            current_word = self.versus_words.pop()
            self.send_string("%s %d %d %d" % (current_word, self.my_versus_score[0], self.other_versus_score[0], current_time))

    def run(self):
        """Main function for handling the client thread"""
        login = self.accept_connection()
        self.login = login
        if not login:
            return
        with ClientConnection.lock:
            highscore = self.game_server.get_highscore(login)
        self.send_string("1 You have been logged in as %s. Your highscore is %d" % (login, highscore))
        print("%s has logged in" % login)
        while True:
            data = self.receive_data()
            if data is None:
                return
            elif data == "s":
                print("%s has started singleplayer" % login)
                score = self.single_player()
                if score is None:
                    return
                print("%s has scored %d" % (login, score))
                if score > highscore:
                    with ClientConnection.lock:
                        self.game_server.update_highscore(login, score)
                    self.send_string("Congratulations! You have beaten your previous highscore of %d. Your new "
                                     "highscore is %d" % (highscore, score))
                    highscore = score
                else:
                    self.send_string("You scored %d" % score)
            elif data == "h":
                with ClientConnection.lock:
                    best = self.game_server.get_best_highscores_string()
                self.send_string(best)
            elif data == "v":
                self.versus_words = []
                self.my_versus_score = [0]
                self.versus_start = False
                self.game_server.add_to_versus_queue(self)
                while not self.versus_start:
                    pass
                score = self.versus()
                if score is None:
                    return
                print("Versus: %s has scored %d, %s has scored %d" % (login, score[0], self.other_login, score[1]))
                if score[0] > highscore:
                    with ClientConnection.lock:
                        self.game_server.update_highscore(login, score[0])
                    message = "# Congratulations! You have beaten your previous highscore of {:d}. Your new highscore " \
                              "is {:d}\n".format(highscore, score[0])
                    highscore = score[0]
                else:
                    message = "# You scored %d\n" % score[0]

                if score[0] > score[1]:
                    message += "You have beaten your opponent {:d} to {:d}".format(*score)
                elif score[0] < score[1]:
                    message += "You have been beaten by your opponent {:d} to {:d}".format(*score)
                else:
                    message += "It's a draw! You both got {:d}".format(score[0])
                self.send_string(message)
            else:
                break
        print("User %s has logged out" % login)
        self.connection.close()
