import socket
import sys
import os
import cv2
import pickle
import numpy as np
import struct
import time
import select

from constants import *
from imgcaption.im2txt.get_imgcaption import ImageCaptioner
#from .imgcaption.im2txt.configuration import ImageCaptioner

def write_caption(image_file, imagecaptioner):
	imagecaptioner.getCaption(image_file)


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
				try:
					data = ""
					payload_size = struct.calcsize("Q")				# Should be 8
					while True:
						begin=time.time()
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
						print(msg_size)

						begin = time.time()
						timedout=False
						while len(data) < msg_size:
							if time.time()-begin > timeout:
								timedout=True
								print('Data receive timed out, clearing...')
								break
							recv_data = conn.recv(16384)
							if (recv_data):
								data += recv_data
								begin = time.time()
							else:
								time.sleep(0.1)
						if timedout:
							data = ""							# Reset
							continue
						frame_data = data[:msg_size]
						data = data[msg_size:]					# Reset

						frame=pickle.loads(frame_data)
						cv2.imwrite(TEMP_COMMU_IMG_LOC,frame)

						captions = IC.getCaption(TEMP_COMMU_IMG_LOC)

						# Write captions
						while os.path.exists(COMMU_IMG_CAPTIONS_LOCK):
							continue
						open(COMMU_IMG_CAPTIONS_LOCK, 'w').close()
						with open(COMMU_IMG_CAPTIONS, 'w') as f:
							for c in captions:
								f.write(' '.join([str(x) for x in c]))
								f.write('\n')
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
	finally:
		print("Closing Image Captioner session")
		IC.closeSession()

if __name__ == "__main__":
	image_process()