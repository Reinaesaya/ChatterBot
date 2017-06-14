import socket
import sys
import os
import cv2
import pickle
import numpy as np
import struct

import multiprocessing
from constants import *
from imgcaption.im2txt.get_imgcaption import ImageCaptioner
#from .imgcaption.im2txt.configuration import ImageCaptioner

def write_caption(image_file, imagecaptioner):
	imagecaptioner.getCaption(image_file)


def image_process(host=RECEIVE_IMAGE_HOST, port=RECEIVE_IMAGE_PORT, model_path=PRETRAINED_MODEL_PATH, vocab_list=PRETRAINED_WORD_COUNTS):
	IC = ImageCaptioner(model_path, vocab_list)
	IC.openSession()
	#captioner = multiprocessing.Process(target=write_caption, args=(TEMP_COMMU_IMG_LOC, IC,))
	print("Image Captioner session and process opened")

	try:
		print('Starting listening port and image processing')
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
		print 'Socket created'
		s.bind((host,port))
		print 'Socket bind complete'

		try:
			s.listen(10)
			print('Socket now listening on '+str(host)+' : '+str(port))

			conn,addr = s.accept()
			print 'Got a connection from '+str(addr[0])+' : '+str(addr[1])
			try:
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

					frame=pickle.loads(frame_data)
					cv2.imwrite(TEMP_COMMU_IMG_LOC,frame)

					captions = IC.getCaption(TEMP_COMMU_IMG_LOC)
					#captioner.start()
					#captioner.join()

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
			except Exception as e:
				print(e)
				if os.path.exists(COMMU_IMG_CAPTIONS_LOCK):
					os.remove(COMMU_IMG_CAPTIONS_LOCK)
				pass
			finally:
				#if captioner.is_alive():
				#	captioner.terminate()
				#	print("Captioner terminated without it finishing")
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