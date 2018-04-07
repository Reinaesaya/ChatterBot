import socket
import sys
import os
import time

import pickle
import struct

import thread

import speech_recognition as sr
from speech_recognition import WaitTimeoutError


def initRecognizer():
	return sr.Recognizer()
	
def listenMessage(recognizer,timeout=None):
	print("Say Something!")
	with sr.Microphone() as source:
		audio = recognizer.listen(source, timeout=timeout)
	
	# recognize speech using Google Cloud Speech
	GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""[insert]"""
	try:
		print("Translating audio")
		message = recognizer.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
		print("Google Cloud Speech thinks you said " + message)
		return message
	except sr.UnknownValueError:
		print("Google Cloud Speech could not understand audio")
		return "*NA*"
	except sr.RequestError as e:
		print("Could not request results from Google Cloud Speech service; {0}".format(e))
		return "*NA*"


# For sending message (client)
def connectSocket(host,port):
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.connect((host, port))
	return serversocket

def sendMessage(serversocket, message):
	return serversocket.sendall(struct.pack("Q", len(message))+message)

def quickTransferMessage(host,port,message):
	serversocket = connectSocket(host,port)
	sendMessage(serversocket, message)
	serversocket.close()


def on_client(conn, addr, target_host, target_port, conntimeout=5):
	print("New client opened at "+str(addr[0])+':'+str(addr[1]))
	conn.settimeout(conntimeout)
	try:
		while True:
			data = ""
			while len(data) == 0:
				data += conn.recv(4096)
			print(str(addr[0])+':'+str(addr[1])+': '+data)
			if "/listen" in data.strip():
				try:
					message = ""
					audiotimeout = int(data.strip().split()[1])
					if audiotimeout <= 0:
						audiotimeout = None
					ss = connectSocket(target_host, target_port)
					r = initRecognizer()
					try:
						message = listenMessage(r,audiotimeout)
						sendMessage(ss, message)
					except WaitTimeoutError:
						print("Listening timed out after: "+str(audiotimeout)+' seconds')
						sendMessage(ss, '*timeout*')
				except Exception as e:
					print(e)
				finally:
					ss.close()
	except Exception as e:
		print(e)
		pass
	finally:
		print "Closing client connection: "+str(addr[0])+':'+str(addr[1])
		conn.close()


# For receiving commands to send image (server)

def run_server(host='', port=8076, target_host='192.168.0.113', target_port=8093):
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

				thread.start_new_thread(on_client,(conn, addr,target_host, target_port, 5,))  # Timeout after an hour

		except Exception as e:
			print(e)
			pass
		finally:
			print "Closing server socket"
			s.shutdown(socket.SHUT_RDWR)
			s.close()

	except Exception as e:
		print(e)

if __name__ == "__main__":
	run_server()
