import socket
import sys
import os
import time

import cv2
import numpy as np
import pickle
import struct

import thread


# For sending image (client)
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
	serversocket = connectSocket(host,port)
	sendImage(serversocket, resizefactor)
	serversocket.close()


def on_client(conn, addr, target_host, target_port, resizefactor, timeout):
	print("New client opened at "+str(addr[0])+':'+str(addr[1]))
	conn.settimeout(timeout)
	try:
		while True:
			data = ""
			while len(data) == 0:
				data += conn.recv(4096)
			print(str(addr[0])+':'+str(addr[1])+': '+data)
			if data.strip() == "/takepicture":
				try:
					ss = connectSocket(target_host, target_port)
					sendImage(ss, resizefactor=resizefactor)
					ss.close()
				except Exception as e:
					print(e)
	except KeyboardInterrupt:
		serveropen = False
	except Exception as e:
		print(e)
		pass
	finally:
		print "Closing client connection: "+str(addr[0])+':'+str(addr[1])
		conn.close()


# For receiving commands to send image (server)

def run_image_capturing_server(host='', port=8075, target_host='192.168.0.113', target_port=8092, resizefactor=1):
	try:
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((host,port))

		try:
			serveropen = True
			while serveropen:
				s.listen(10)
				print('Socket now listening on '+str(host)+' : '+str(port))

				conn,addr = s.accept()
				print 'Got a connection from '+str(addr[0])+' : '+str(addr[1])

				thread.start_new_thread(on_client,(conn, addr,target_host, target_port, resizefactor, 3600,))  # Timeout after an hour

		except Exception as e:
			print(e)
			pass
		finally:
			print "Closing server socket"
			s.shutdown(socket.SHUT_RDWR)
			s.close()

	except Exception as e:
		print(e)
		pass

if __name__ == "__main__":
	#serversocket = connectSocket('192.168.0.113',8092)
	#try:
		#sendImage(serversocket, resizefactor=0.5)
	#	sendImagebyInterval(serversocket, interval=0.5, resizefactor=0.50)
		#sendVid(serversocket, resizefactor=0.25)
	#except Exception as e:
	#	print(e)
	#serversocket.close()


	run_image_capturing_server(resizefactor=0.5)

	##
