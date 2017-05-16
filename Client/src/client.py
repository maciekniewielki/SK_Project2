import socket

def login(s):
	log = raw_input('Login: ')
	passw = raw_input('Password: ')
	s.send('l '+log+' '+passw)
	data = s.recv(BUFFER_SIZE)
	success,message = data.split(' ',1)
	return success, message
def register(s):
	log = raw_input('Login: ')
	passw = raw_input('Password: ')
	s.send('r '+log+' '+passw)
	success,message = data.split(' ',1)
	return success, message
def quitance(s):
	print('See ya later, aligator!')
	s.close()
	exit()

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
print('Welcome to Typespeed 1.0!')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
a = [login,register,quitance]
while 1:
	print('Choose an option:')
	print('1 - log in')
	print('2 - register')
	print('3 - exit')
	wybor = input()
	if wybor!= 1 or wybor!= 2 or wybor != 3
		print('Wrong choice, try again')
	else
		success, message = a[wybor-1](s)


