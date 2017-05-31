import constants
import socket

def highscore(s):
	s.send('h')
	scores = s.recv(constants.BUFFER_SIZE)
	print('The best players on the server are:')
	print(scores)
	
