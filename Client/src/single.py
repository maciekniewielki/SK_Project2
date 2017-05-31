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
	
	while True:
		wordIn = s.recv(constants.BUFFER_SIZE)
		tim=time() - timer
		if tim>60:
			break
		line = 'type: {:<30} time:{:>1}'.format(wordIn,int(round(tim))) 
		print(line)
		wordOut=raw_input()
		while not wordOut:
			wordOut=raw_input()
		s.send(wordOut)
	finish(s)
def finish(s):
	s.send('#')
	print('Time is up!')
	result=s.recv(constants.BUFFER_SIZE)
	print(result)
