import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new

HOST=''
PORT=8090

#HOST = socket.gethostbyname(socket.gethostname())
#HOST = "192.168.1.105"

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print 'Socket created'

s.bind((HOST,PORT))
print 'Socket bind complete'

try:
	s.listen(10)
	print 'Socket now listening on '+str(HOST)+" : "+str(PORT)

	conn,addr=s.accept()
	print 'Got a connection from '+str(addr[0])+' : '+str(addr[1])
	try:
		### new
		data = ""
		payload_size = struct.calcsize("Q")
		#print(payload_size)
		while True:
			while len(data) < payload_size:
				data += conn.recv(4096)
			packed_msg_size = data[:payload_size]
			data = data[payload_size:]
			msg_size = struct.unpack("Q", packed_msg_size)[0]
			print(msg_size)
			while len(data) < msg_size:
				data += conn.recv(4096)
			frame_data = data[:msg_size]
			data = data[msg_size:]
			###

			frame=pickle.loads(frame_data)
			#cv2.imwrite('commu_pic.jpg',frame)
			cv2.imshow('frame',frame)
			if cv2.waitKey(1) == 27:
				break
	except Exception as e:
		print(e)
	finally:
		print "Closing client connection"
		conn.close()
except Exception as e:
	print(e)
finally:
	print "Closing server socket"
	s.close()