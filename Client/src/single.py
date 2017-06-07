#importing the packages necessary to run these functions
import socket
from time import sleep, time
#importing constant values and the sending and receiving functions
import constants
#function initiating the single mode game
def start(s):
	constants.sending(s,'s')
	print('3...')
	sleep(1)
	print('2...')
	sleep(1)
	print('1...')
	sleep(1)
	play(s)
#function handling the single player playing 
def play(s):
	timer = time()
#loop for sending and receiving words
	while True:
		wordIn = constants.receive(s)
		tim=time() - timer
		if tim>60:
			break
		line = 'type: {:<30} time:{:>1}'.format(wordIn,int(round(tim))) 
		print(line)
		wordOut=raw_input()
		while not wordOut:
			wordOut=raw_input()
		constants.sending(s,wordOut)
	finish(s)
#function finishing the game with sending '#' to the server and printing out the score message from it
def finish(s):
	constants.sending(s,'#')
	print('Time is up!')
	result=constants.receive(s)
	print(result)
