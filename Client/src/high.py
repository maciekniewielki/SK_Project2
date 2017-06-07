import constants
import socket
#function for requesting from the server a message with 3 top players on the server
#the server formats the message
def highscore(s):
	constants.sending(s,'h')
	scores = constants.receive(s)
	print('The best players on the server are:')
	print(scores)
	
