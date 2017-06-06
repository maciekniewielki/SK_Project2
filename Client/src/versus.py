import socket
from time import sleep
import constants

def start(s):
	constants.sending(s,'v')
	print('Waiting for the other player')
	nickname = constants.receive(s)
	print('Connected to '+nickname)
	print('3...')
	sleep(1)
	print('2...')
	sleep(1)
	print('1...')
	sleep(1)
	play(s,nickname)
def play(s,nickname):
	while True:
		message = constants.receive(s)
		if message[0] =='#':
			print("Waiting for your opponent to finish")
			break
		wordIn,scoreY,scoreO, tim = message.split(' ')
		line = 'type: {:<20} time: {} {:>10}: {} You: {}'.format(wordIn,tim,nickname,scoreO,scoreY) 
		print(line)
		wordOut=raw_input()
		while not wordOut:
			wordOut=raw_input()
		constants.sending(s,wordOut)
	finish(s,message)
def finish(s, message):
	print('Time is up!')
	harsh,result = message.split(' ',1)
	print(result)

