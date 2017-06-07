#constant values used throughout the client
SERVER_PORT = 30005
BROADCAST_PORT = 30006
BUFFER_SIZE = 1024
import socket
#functions for sending are defined here to avoid confusion with all the try catches
#and for error handling
def sending(s, message):
	try:
		s.send(message)
	except socket.error:
		print("Lost connection to the server")
		exit()
		
def receive(s):
	try:
		message = s.recv(BUFFER_SIZE)
		return message
	except socket.error:
		print("Lost connection to the server")
		exit()
	
