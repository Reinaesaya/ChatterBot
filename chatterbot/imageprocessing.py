import socket
import sys
import os
import cv2
import pickle
import numpy as np
import struct
import time
import select
import thread

from constants import *
from imgcaption.im2txt.get_imgcaption import ImageCaptioner
#from .imgcaption.im2txt.configuration import ImageCaptioner

def write_caption(image_file, imagecaptioner):
	imagecaptioner.getCaption(image_file)


def on_client(conn, addr, ImageCaptionerObject, timeout):
	print("New client opened at "+str(addr[0])+':'+str(addr[1]))
	conn.settimeout(timeout)
	try:
		payload_size = struct.calcsize("Q")				# Should be 8
		while True:
			data = ""
			print("Waiting for payload data...")
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
			print("Got payload data")
				
			packed_msg_size = data[:payload_size]
			data = data[payload_size:]
			msg_size = struct.unpack("Q", packed_msg_size)[0]
			print(str(addr[0])+':'+str(addr[1])+': '+str(msg_size))

			try:
				print("Waiting to get entire frame...")
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

			except Exception as e:
				print(e)
				data = ""
				continue

			print("Got entire frame")
			frame_data = data[:msg_size]
			data = data[msg_size:]					# Reset

			frame=pickle.loads(frame_data)
			cv2.imwrite(TEMP_COMMU_IMG_LOC,frame)

			print("Getting captions...")
			captions = ImageCaptionerObject.getCaption(TEMP_COMMU_IMG_LOC)

			# Write captions
			print("Writing captions")
			while os.path.exists(COMMU_IMG_CAPTIONS_LOCK):
				continue
			open(COMMU_IMG_CAPTIONS_LOCK, 'w').close()
			with open(COMMU_IMG_CAPTIONS, 'w') as f:
				f.write(str(time.time()))
				for c in captions:
					f.write('\n')
					f.write(' '.join([str(x) for x in c]))
			os.remove(COMMU_IMG_CAPTIONS_LOCK)

			#cv2.imshow('frame',frame)
			#if cv2.waitKey(1) == 27:
			#	break
	except KeyboardInterrupt:
		serveropen = False
	except Exception as e:
		print(e)
		pass
	finally:
		# Remove lock file for image
		if os.path.exists(COMMU_IMG_CAPTIONS_LOCK):
			os.remove(COMMU_IMG_CAPTIONS_LOCK)
		print "Closing client connection: "+str(addr[0])+':'+str(addr[1])
		conn.close()



def image_process(host=RECEIVE_IMAGE_HOST, port=RECEIVE_IMAGE_PORT, timeout=RECV_TIMEOUT, model_path=PRETRAINED_MODEL_PATH, vocab_list=PRETRAINED_WORD_COUNTS):
	IC = ImageCaptioner(model_path, vocab_list)
	IC.openSession()
	print("Image Captioner session and process opened")

	try:
		print('Starting listening port and image processing')
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print 'Socket created'
		s.bind((host,port))
		print 'Socket bind complete'

		try:
			serveropen = True
			while serveropen:
				s.listen(10)
				print('Socket now listening on '+str(host)+' : '+str(port))

				conn,addr = s.accept()
				print 'Got a connection from '+str(addr[0])+' : '+str(addr[1])

				thread.start_new_thread(on_client,(conn, addr, IC, timeout,))
				#on_client(conn, addr, IC, timeout=timeout)

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
	finally:
		print("Closing Image Captioner session")
		IC.closeSession()

if __name__ == "__main__":
	image_process()