import cv2
import numpy as np
import socket
import sys
import time
import pickle
import struct

def connectSocket(host,port):
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.connect((host, port))
	return serversocket

def sendImage(serversocket, cam_port=0, resizefactor=1):
	cap = cv2.VideoCapture(cam_port)
	ret, frame = cap.read()
	sendFrame(serversocket, frame, resizefactor)
	cap.release()

def sendImagebyInterval(serversocket, interval=1, cam_port=0, resizefactor=1, period=-1):
	if period < 0:
		while True:
			sendImage(serversocket, cam_port, resizefactor)
			time.sleep(interval)
	else:
		begin = time.time()
		now = time.time()
		while now-begin < period:
			sendImage(serversocket, cam_port, resizefactor)
			time.sleep(interval)
			now = time.time()

def sendVid(serversocket, cam_port=0, resizefactor=1, period=-1):
	cap = cv2.VideoCapture(cam_port)
	if period < 0:
		while True:
			ret, frame = cap.read()
			sendFrame(serversocket, frame, resizefactor)
	else:
		begin = time.time()
		now = time.time()
		while now-begin < period:
			ret, frame = cap.read()
			sendFrame(serversocket, frame, resizefactor)
			now = time.time()
	cap.release()

def sendFrame(serversocket, frame, resizefactor=1):
	frame = cv2.resize(frame, (0,0), fx=resizefactor, fy=resizefactor)
	data = pickle.dumps(frame)
	print(len(data))
	return serversocket.sendall(struct.pack("Q", len(data))+data)

def quickTransferSnapshot(host,port,resizefactor=1):
	serversocket = connectSocket('192.168.0.113',8092)
	sendImage(serversocket, resizefactor)
	serversocket.close()	

if __name__ == "__main__":
	serversocket = connectSocket('192.168.0.113',8092)
	try:
		#sendImage(serversocket, resizefactor=0.5)
		sendImagebyInterval(serversocket, interval=0.5, resizefactor=0.50)
		#sendVid(serversocket, resizefactor=0.25)
	except Exception as e:
		print(e)
	serversocket.close()

