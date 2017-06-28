import socket
import sys
import os
import time

import client_cv

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
				try:
					while True:
						data = ""
						while len(data) == 0:
							data += conn.recv(4096)
						print(data)
						if data.strip() == "/takepicture":
							try:
								ss = client_cv.connectSocket(target_host, target_port)
								client_cv.sendImage(ss, resizefactor=resizefactor)
								ss.close()
							except Exception as e:
								print(e)
				except KeyboardInterrupt:
					serveropen = False
				except Exception as e:
					print(e)
					pass
				finally:
					print "Closing client connection"
					conn.close()

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
	run_image_capturing_server()