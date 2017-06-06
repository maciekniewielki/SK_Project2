import constants
import socket

def highscore(s):
	constants.sending(s,'h')
	scores = constants.receive(s)
	print('The best players on the server are:')
	print(scores)
	
