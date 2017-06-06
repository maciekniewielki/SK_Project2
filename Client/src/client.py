import socket
import constants
import single
import high
import sys
import versus

def login(s):
	log = raw_input('Login: ')
	passw = raw_input('Password: ')
	constants.sending(s,'l '+log+' '+passw)
	data = constants.receive(s)
	success,message = data.split(' ',1)
	return success, message
def register(s):
	log = raw_input('Login: ')
	passw = raw_input('Password: ')
	constants.sending(s,'r '+log+' '+passw)
	data =constants.receive(s)
	success,message = data.split(' ',1)
	return success, message
def quitance(s):
	print('See ya later, aligator!')
	s.close()
	exit()
def mainMenu():
	print('Choose an option:')
	print('1 - log in')
	print('2 - register')
	print('3 - exit')
	return raw_input()
def loggedInMenu():
	print('Choose an option:')
	print('1 - single')
	print('2 - versus')
	print('3 - show highscores')
	print('4 - exit')
	return raw_input()

a = [login,register,quitance]




try:
	SERVER_IP = sys.argv[1]
except:
	print("No server IP given, trying to find a server via broadcast")
	addr = ('<broadcast>', constants.BROADCAST_PORT) 
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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.connect((SERVER_IP, constants.SERVER_PORT))
except socket.error:
	print('No server found :(')
	exit()

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

