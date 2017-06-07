Typespeed 2.0 the game created by Maciej Buczyński and Alicja Przybyś as a project for
Computer Networks laboratories.

To start the server simply navigate to the Server/src folder and run server.py with Python 3

To start the client navigate to the Client/src folder. Run client.py with Python 2. You can put 
the server IP address as an argument when running the application, if you don't the application 
will search for the server sending a message over broadcast. Beware, some networks have firewalls
set up preventing broadcast messages from being sent.

When you connect successfully to the server, you will enter the main Menu. You may choose to log in,
if you're already a registered user or to register on the server or to exit the application.

Once you achieve that, you will enter the next menu which will allow you to play the game in 
the single player mode, versus mode, show the top five players' highscore or exit the application.

SINGLE PLAYER
In single player you play to beat your own high score. The server provides you with words to type in
and you have 60 seconds to type in as many words correctly as you can. If you type a word in incorrectly 
you will be asked to rewtype the word. To submit the word press ENTER.

VERSUS
When you choose the versus mode you are put in the queue to be paired up with another player on the
server who wishes to play a versus game. Once you're connected both of you receive the same words to be
typed in. You are provided with the information about your current score as well as your opponent's score
as you play the game. If you beat your highscore through the versus game this information is saved on the
server as well.

Note that currently the maximum number of connections to the server is 10, however that can easily be
changed in the Server/src/constants.py file by altering the MAX_CONNECTIONS variable.
