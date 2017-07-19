import socket
import sys
import os
import time

import pickle
import struct

import thread


# For sending (client)
def sendListenCommand(commandsocket, timeout=0):
	command = "/listen "+str(timeout)
	commandsocket.sendall(command)

def connectMicrophoneSocket(host,port):
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.connect((host, port))
	return serversocket


# For receiving
def openReceiveSocket(host, port):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host,port))
	return s

def getMessage(receivesocket, timeout=60):
	receivesocket.listen(10)
	conn,addr = receivesocket.accept()
	conn.settimeout(timeout)
	try:
		data = ""
		payload_size = struct.calcsize("Q")	
		begin = time.time()
		while len(data) < payload_size:
			recv_data = conn.recv(4096)
			if recv_data:
				data += recv_data
			else:
				if time.time()-begin > timeout:
					print("Payload size data receive timeout. Likely that connection is closed. Restarting...")
					raise Exception('Data Timeout, Restarting Connection')
				else:
					time.sleep(0.1)
				
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack("Q", packed_msg_size)[0]

		try:
			begin = time.time()
			while len(data) < msg_size:
				if time.time()-begin > timeout:
					raise Exception('Data receive timed out, clearing...')
				recv_data = conn.recv(16384)
				if (recv_data):
					data += recv_data
					begin = time.time()
				else:
					time.sleep(0.1)
			message = str(data[:msg_size])
		except Exception as e:
			print(e)
			message = "*error*"
	except Exception as e:
		print(e)
		message = "*error*"
		pass
	finally:
		print "Closing client connection: "+str(addr[0])+':'+str(addr[1])
		conn.close()
		return message


if __name__ == "__main__":
	rs = openReceiveSocket(host='', port=8093)

	try:
		ms = connectMicrophoneSocket(host='192.168.1.144', port=8076)
		try:
			sendListenCommand(ms, 5)
		except:
			print("Here: "+e)
			pass
		finally:
			ms.close()

		message = getMessage(rs)
		print(message)
	except Exception as e:
		print("Here1: "+e)	
		pass
	finally:
		rs.shutdown(socket.SHUT_RDWR)
		rs.close()

	##
