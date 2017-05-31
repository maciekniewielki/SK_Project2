import threading

from resources.errors import NameTaken, ValidationException

import resources.constants as constants


class ClientConnection(threading.Thread):
    lock = threading.Lock()

    def __init__(self, game_server, connection, address):
        super().__init__()
        self.game_server = game_server
        self.connection = connection
        self.address = address

    def receive_data(self):
        try:
            data = self.connection.recv(constants.BUFFER_SIZE).decode()
        except ConnectionAbortedError:
            print("User %s has disconnected" % (self.address,))
            self.connection.close()
            return None
        return data

    def send_string(self, s):
        self.connection.send(s.encode())

    def try_login(self, login, password):
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
        try:
            with ClientConnection.lock:
                self.game_server.register_user(login, password)
        except (ValidationException, NameTaken) as e:
            self.send_string("0 %s" % e.value)
            return False
        return True

    def accept_connection(self):
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
                    score += 1
                    correct = True
                else:
                    self.send_string(current_word)
            current_word = words.pop()
            self.send_string(current_word)

    def run(self):
        login = self.accept_connection()
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
            else:
                break
        print("User %s has logged out" % (self.address,))
        self.connection.close()
