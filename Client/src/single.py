import socket
from time import sleep, time
import constants

def start(s):
	s.send('s')
	print('3...')
	sleep(1)
	print('2...')
	sleep(1)
	print('1...')
	sleep(1)
	play(s)

def play(s):
	timer = time()
	
	while time() - timer < 60:
		wordIn = s.recv(constants.BUFFER_SIZE)
		print(WordIn)
		wordOut=input()
		s.send(wordOut)
	finish(s)
def finish(s):
	s.send('#')
	print('Koniec gry')
