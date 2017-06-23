import cv2
import numpy as np
import socket
import sys
import time
import pickle
import struct

def connectSocket(host,port):
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientsocket.connect((host, port))
	return clientsocket

def sendImage(clientsocket, cam_port=0):
	cap = cv2.VideoCapture(cam_port)
	ret, frame = cap.read()
	data = pickle.dumps(frame)
	print(len(data))
	clientsocket.sendall(struct.pack("Q", len(data))+data)
	cap.release()

if __name__ == "__main__":
	clientsocket = connectSocket('192.168.0.113',8092)
	while True:
		try:
			sendImage(clientsocket)
			time.sleep(1)
		except:
			break
	clientsocket.shutdown(socket.SHUT_RDWR)
	clientsocket.close()

