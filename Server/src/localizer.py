import threading
import resources.constants as constants
import socket


class Localizer(threading.Thread):

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", constants.LOCALIZER_PORT))
        print("Localizer started")
        while 1:
            data, addr = s.recvfrom(1024)
            data = data.decode()
            if data == "Any typespeed servers around?":
                s.sendto("I'm here!".encode(), addr)
                print("%s asked for server ip" % addr[0])
