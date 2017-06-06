SERVER_PORT = 30005
BROADCAST_PORT = 30006
BUFFER_SIZE = 1024
import socket
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
	
