
### For Image Captioning ###

CHATTERBOT_FOLDER_LOC = "/home/user2/Desktop/OUIRL-ChatBot/chatterbot"

PRETRAINED_MODEL_PATH = CHATTERBOT_FOLDER_LOC+"/imgcaption/pretrained_model/model.ckpt-2000000"
PRETRAINED_WORD_COUNTS = CHATTERBOT_FOLDER_LOC+"/imgcaption/pretrained_model/word_counts.txt"

TEMP_COMMU_IMG_LOC = CHATTERBOT_FOLDER_LOC+"/imgcaption/commu_pic.jpg"
COMMU_IMG_CAPTIONS = CHATTERBOT_FOLDER_LOC+"/imgcaption/commu_pic_caps.txt"
COMMU_IMG_CAPTIONS_LOCK = CHATTERBOT_FOLDER_LOC+"/imgcaption/commu_pic_caps.lock"

# For control conditions
CTRL_TEMP_COMMU_IMG_LOC = CHATTERBOT_FOLDER_LOC+"/imgcaption/sample_captions/commu_pic.jpg"
CTRL_COMMU_IMG_CAPTIONS = CHATTERBOT_FOLDER_LOC+"/imgcaption/sample_captions/commu_pic_caps.txt"
CTRL_COMMU_IMG_CAPTIONS_LOCK = CHATTERBOT_FOLDER_LOC+"/imgcaption/sample_captions/commu_pic_caps.lock"

CTRL_RANGE = (1,3)		# Min, Max
CONVOSTART_FORCE = 3


### For CommU Robot ###
RECEIVE_IMAGE_HOST = ''
RECEIVE_IMAGE_PORT = 8092
RECV_TIMEOUT = 4

SEND_COMMAND_HOST = '192.168.1.83'
SEND_COMMAND_PORT = 8079

CUSTOM_SEND_COMMAND_HOST = SEND_COMMAND_HOST
CUSTOM_SEND_COMMAND_PORT = 8075

GREETINGS = ['hi', 'hello']


### For Microphone ###
RECEIVE_AUDIO_HOST = ''
RECEIVE_AUDIO_PORT = 8093
RECV_AUDIO_TIMEOUT = 7

SEND_LISTENCOMMAND_HOST = '192.168.1.144'
SEND_LISTENCOMMAND_PORT = 8076