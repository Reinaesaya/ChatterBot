
### For Image Captioning ###

CHATTERBOT_FOLDER_LOC = "/home/user2/Desktop/OUIRL-ChatBot/chatterbot"

PRETRAINED_MODEL_PATH = CHATTERBOT_FOLDER_LOC+"/imgcaption/pretrained_model/model.ckpt-2000000"
PRETRAINED_WORD_COUNTS = CHATTERBOT_FOLDER_LOC+"/imgcaption/pretrained_model/word_counts.txt"

TEMP_COMMU_IMG_LOC = CHATTERBOT_FOLDER_LOC+"/imgcaption/commu_pic.jpg"
COMMU_IMG_CAPTIONS = CHATTERBOT_FOLDER_LOC+"/imgcaption/commu_pic_caps.txt"
COMMU_IMG_CAPTIONS_LOCK = CHATTERBOT_FOLDER_LOC+"/imgcaption/commu_pic_caps.lock"


### For CommU Robot ###
RECEIVE_IMAGE_HOST = ''
RECEIVE_IMAGE_PORT = 8092

SEND_COMMAND_HOST = '192.168.1.83'
SEND_COMMAND_PORT = 8079

GREETINGS = ['hi', 'hello']