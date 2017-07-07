# OUIRL-ChatBot

The OUIRL (Osaka University Intelligent Robotics Laboratory) ChatBot is an experimental fork upon this opensource [ChatterBot](https://github.com/gunthercox/ChatterBot). Additions upon the original API will include adding adapters for various online chatterbots, and trial implementation of visual stimuli through image/video captioning for conversation manipulation.


## Setup:

1) Please refer to the original Github repo for setup procedures, though simple cloning of repository and execution of following command should be sufficient. There are also various modules that need to be installed through pip: 

```
# Original ChatterBot setup installations
python setup.py install

# Enhancements

## Mechanize used for interaction with online chatbot platforms
pip install mechanize

## Google Text to Speech for creating mp3 files from chatbot responses
pip install gTTS

## Pygame for playing mp3 audio and evaluating video input
pip install pygame

## Speech to Text
pip install SpeechRecognition

sudo apt-get install python-pyaudio python3-pyaudio

pip install --upgrade google-api-python-client

```

2) Navigate to [/chatterbot/imgcaption/](chatterbot/imgcaption) and follow the setup precedures there to implement image captioning


## Running

To run terminal-based example module, simply run:

```
# To train
python TatoraChat1.py -train

# To run without training conversation into database
python TatoraChat.py -readonly

# To use CommU movement and voice
python TatoraChat.py -commumove -commutalk


python TatoraChat.py
```


# License

ChatterBot is licensed under the [BSD 3-clause license](https://opensource.org/licenses/BSD-3-Clause).
