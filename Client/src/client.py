import socket
import constants
import single
import high

def login(s):
	log = raw_input('Login: ')
	passw = raw_input('Password: ')
	s.send('l '+log+' '+passw)
	data = s.recv(constants.BUFFER_SIZE)
	success,message = data.split(' ',1)
	return success, message
def register(s):
	log = raw_input('Login: ')
	passw = raw_input('Password: ')
	s.send('r '+log+' '+passw)
	data = s.recv(constants.BUFFER_SIZE)
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

print('Welcome to Typespeed 1.0!')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.connect((constants.SERVER_IP, constants.SERVER_PORT))
except (ConnectionRefusedError, TimeoutError):
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
	elif wyborLog == 2:
		print('Currently under construction')
	elif wyborLog == 1:
		single.start(s)
	elif wyborLog == 3:
		high.highscore(s)
	else:
		quitance(s)

