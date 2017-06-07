#importing the basic python packages necessary for the running of the application
import socket
import sys
#importing functions put in different files
import constants
import single
import high
import versus

#function to log into the game, it sends 'l' to the server and prints out the server's response
def login(s):
	log = raw_input('Login: ')
	passw = raw_input('Password: ')
	constants.sending(s,'l '+log+' '+passw)
	data = constants.receive(s)
	success,message = data.split(' ',1)
	return success, message
#function to register a new user, it sends 'r' to the server and prints out the server's response
def register(s):
	log = raw_input('Login: ')
	passw = raw_input('Password: ')
	constants.sending(s,'r '+log+' '+passw)
	data =constants.receive(s)
	success,message = data.split(' ',1)
	return success, message
#function to exit the application
def quitance(s):
	print('See ya later, aligator!')
	s.close()
	exit()
#function printing out the main menu options 
def mainMenu():
	print('Choose an option:')
	print('1 - log in')
	print('2 - register')
	print('3 - exit')
	return raw_input()
#function printing out the menu for when you manage to log in
def loggedInMenu():
	print('Choose an option:')
	print('1 - single')
	print('2 - versus')
	print('3 - show highscores')
	print('4 - exit')
	return raw_input()

#array of functions
a = [login,register,quitance]

#getting the server ip either via the second argument or via broadcast
try:
	SERVER_IP = sys.argv[1]
except:
	print("No server IP given, trying to find a server via broadcast")
	addr = ('<broadcast>', constants.BROADCAST_PORT) 
#setting up a UDP socket for broadcasting the message
	UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	UDPSock.settimeout(5)
	UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	UDPSock.sendto("Any typespeed servers around?", addr)
	try:
		UDPdata, SERVER_addr = UDPSock.recvfrom(constants.BUFFER_SIZE)
	except socket.timeout:
		print("No server found via broadcast, perhaps your firewall is not allowing a broadcast connection.")
		print("Try running the client application with the server IP as an argument")
		exit()
	UDPSock.close()	
	if not UDPdata=="I'm here!":
		print("Wrong server")
		exit()
	SERVER_IP=SERVER_addr[0]

print('Welcome to Typespeed 2.0!')
#setting up the TCP socket with the server IP 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.connect((SERVER_IP, constants.SERVER_PORT))
except socket.error:
	print('No server found :(')
	exit()
#main menu loop allowing for errors in logging in
while 1:
	wybor = int(mainMenu())
	if not wybor in [1,2,3]:
		print('Wrong choice, try again')
	else:
		success, message = a[wybor-1](s)
		if success=='1':
			break
		else:
			print(message)
			
print(message)
#logged in menu loop allowing to play the game
while 1:
	wyborLog=int(loggedInMenu())
	if not wyborLog in [1,2,3,4]:
		print('Wrong choice, try again')
	elif wyborLog == 1:
		single.start(s)
	elif wyborLog == 2:
		versus.start(s)
	elif wyborLog == 3:
		high.highscore(s)
	else:
		quitance(s)

