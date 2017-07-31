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
	GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "tribal-primacy-107411",
  "private_key_id": "39fabbaf6fa0021157a3a0815c96dcd8fc30896f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDduJrcSkuaZi+X\nTr0k1pnXQwoeDf5wWZJNP+t7RgOOHZG/fT6ALjh4KKl2JZfNa+B+ioVCNiKzgMkJ\nG6HTaPS54ZDVDyxHXBNTXgkMnN5aREHC1phG5sg4GsJeNvnxgraNZIacTSsp/Nhs\nBSBGtDWvZJyum6aHwcqa/reuMm96bOZ3atOyQvIOVb66MxTs/pqosMyUVUplzUQQ\njoCu1GVUfe2/dJT/mn+YNJsNfn5OchWGi7DhQvnMPbO2TFWcewgw3wnZkzTRm88A\ndthlDjPaVRGNyoc6PcaW4T/I9r7Xx4IdlC1Zp3wr67N8eWRmh35zqtIg25axrCGA\ndlOuHKARAgMBAAECgf8J6qsCfBz/JHlJPmK3T+HeZUebXVGqZ/DJnVJEitBRF7St\nG+Ai9SF31/NV+9h0sTgZPZjR0IBwBt9dYoVnLz3C32CnwHktt+O+/TW3NEzw1jZN\n88sok90T2ITymDYVpAMGNlJokaSclb9Le+81oMAsWBOp7sxD+VojR8E8L7h/55Z2\n6Dzsv/Q0AccBKWuwI31S+wzUuaIEnNB3rZtNmXimfNJvgE3kmPwIgztTEMKguscI\njjJBKydem8lmijzdNpQS/a/QxshfSnTichPQKnMG+k8X9rGKd75PSZn6sJuxSvd3\nUAeUSg1xzOSRPXhbo0CYwHFkQ6LczazKYd6rhp0CgYEA+pFgx0pivMm+yC8jUfTt\nrLPcFpzCwZMelM0TTQjUz6mNMwMo2mb0hc0FzwVEGuVqZrmv5qJts6AM7EQi1LfB\n3ISD25QMJvfN6BR0T2yi/ds2QgO3tb2O4Dl6EInuW0Wdkz0N+d+BY9oi4i8Lm9E8\nG52EM0rB75zgBXuSXMalzt0CgYEA4ocheCCaQX+YhEKj4SftqFxYFLqkHIoe3qlg\n8zqKxtvt/mkNWpZe7wr3r0FNu9/BIsVqN5N2EMdNtD0F/gHEhEUTY8kkt8z7F4q0\nA75whYXH7CB8MGhPHIcxRljwE3mMGka3fFKZpYmdgGrgFuEi6VWASOfTuF7Pvj/6\nF0V3MMUCgYEA8MyhmySLey7O4AcdBHhDqUM4caq5J9rA+vOSZufjzKX/AlU4/5sN\nx0BfIrLG3qo29P3iY90ZXBSmFrDsYE0wS0I2jeDbRN/EzBJMLMAUa64tmIeGF2xS\nUH4sJpTHsoNWideVBNuct189Qu0/VMFh6JAaKkjf0+yJBfvZjruBQSkCgYA2AfO3\n2UYNwacSOXUq9EMUNdgGMS15ZHDRs15a/yUhHkRSuKcnZtyBb4L39MDcvw8kBB87\n2tt2Sp47D6WDFtbMlk92JfmsHKHszfP3RIs9OlUc9e3F+MiLy6uy0veCHSOLDDso\n1+Sr8/BqMpD0w354VRs9xo/S0EAFYul0bOpq5QKBgQDuCYD/ifNf4C+NsTcTlOJY\nuleXKQyTDxyIpPn7nVasP85xVq62lAwuzpJyYOqujMvb1XEKxOEXIcpluiu8LU9s\nBYGfS9gKtjbsPWGhd9JfSe1DBsiTOfobHcOhAn8hOotL07kpZ1NpeXAD0TTtS03m\n1iZardZS8cyjSeH8CgHkCw==\n-----END PRIVATE KEY-----\n",
  "client_email": "tribal-primacy-107411@appspot.gserviceaccount.com",
  "client_id": "111168719916558691174",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tribal-primacy-107411%40appspot.gserviceaccount.com"
}"""
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