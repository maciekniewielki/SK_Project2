import socket
from time import sleep
import constants
#start of the versus game with awaiting to be matched with another player
def start(s):
	constants.sending(s,'v')
	print("Entering a versus game")
	print('Type in the given words as fast as you can')
	print('Press ENTER to submit your answer')
	print('You will be asked to retype the words you spell incorrectly')
	print('Waiting for the other player')
	nickname = constants.receive(s)
	print('Connected to '+nickname)
	print('3...')
	sleep(1)
	print('2...')
	sleep(1)
	print('1...')
	sleep(1)
	play(s,nickname)
#the function play requires a socket and the opponent's nickname
def play(s,nickname):
#the loop allowing to play, here timing is handled by the server
	while True:
		message = constants.receive(s)
#it might happen that the other player takes longer to finish as the server needs the last word sent in
		if message[0] =='#':
			print("Waiting for your opponent to finish")
			break
		wordIn,scoreY,scoreO, tim = message.split(' ')
		line = 'type: {:<20} time: {} {:>10}: {} You: {}'.format(wordIn,tim,nickname,scoreO,scoreY) 
		print(line)
		wordOut=raw_input()
#The client does not allow for sending empty messages
		while not wordOut:
			wordOut=raw_input()
		constants.sending(s,wordOut)
	finish(s,message)
#function dealing with  finishing of the game and score printing
#the score is given after the "#" symbol which allows the client to see when the timer has run out
def finish(s, message):
	print('Time is up!')
	harsh,result = message.split(' ',1)
	print(result)

