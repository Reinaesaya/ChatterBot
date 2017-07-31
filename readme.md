# OUIRL-ChatBot

The OUIRL (Osaka University Intelligent Robotics Laboratory) ChatBot is an experimental fork upon this opensource [ChatterBot](https://github.com/gunthercox/ChatterBot). Additions upon the original API will include adding adapters for various online chatterbots, and trial implementation of visual stimuli through image/video captioning for conversation manipulation.


## Setup:

The primary chatterbot is processed within a Linux server with a GPU. Voice recognition is done through a microphone plugged into a Windows OS. Image capture and text-to-speech embedded in CommU Robot

1) Please refer to the original Github repo for simple setup procedures. There are also a number of separate setup processes that need to be done in order to fully run the demo.

  * Download and install Anaconda2 in both Linux and Windows. Git clone repository into both.
  * Do the following:
```
# Linux, in top folder

## Original ChatterBot setup installations
python setup.py install

## Enhancements

### Mechanize used for interaction with online chatbot platforms
pip install mechanize

### Google Text to Speech for creating mp3 files from chatbot responses
pip install gTTS

### Pygame for playing mp3 audio and evaluating video input
pip install pygame



# Windows, in top folder

## Speech to Text
pip install SpeechRecognition
sudo apt-get install python-pyaudio python3-pyaudio
pip install --upgrade google-api-python-client

```

   * Setup CommU robot. Link it to the local WiFi connection. Figure out all the host IPs and ports and change them in ```/chatterbot/constants.py```, ```/chatterbot/imgcaption/commu_imgcapture.py```, and in ```/chatterbot/speech_recognition_socket.py```
   * ```scp``` ```commu_imgcapture.py``` into CommU home directory
   * Install opencv2 into CommU. Make reference to this: [http://www.instructables.com/id/Getting-Started-With-OpenCV-and-Intel-Edison/](http://www.instructables.com/id/Getting-Started-With-OpenCV-and-Intel-Edison/)

2) Navigate to [/chatterbot/imgcaption/](chatterbot/imgcaption) and follow the setup precedures there to implement image captioning

3) Setup up your own Google Cloud Speech API credentials and replace them into the ```GOOGLE_CLOUD_SPEECH_CREDENTIALS``` variable in speech_recognition_socket.py in Windows. I made reference to this when setting it up: [https://pythonspot.com/en/speech-recognition-using-google-speech-api/](https://pythonspot.com/en/speech-recognition-using-google-speech-api/)


## Running

1) Initialize CommU image capturing listening and response port
```
# In home directory
python commu_imgcapture.py
```

2) Start imageprocessing process (in its own terminal)
```
# In Linux, within Anaconda2, under /chatterbot folder
python imageprocessing.py
```

3) Initialize voice to Speech to Text listening and response port (not strictly necessary if you don't want TatoraVoiceAdapter
```
# In Windows, within Anaconda2, under /chatterbot folder
python speech_recognition_socket.py
```

4) Change path variables in ```constants.py``` and ```TatoraChat1.py``` as they are hardcoded

5) Running

```
# All in Linux, top folder
## To train
python TatoraChat1.py -train

## To run with just terminal text input and no CommU
python TatoraTalk.py -terminal

## To use CommU and Windows microphone
python TatoraTalk.py -commumove -commutalk

## To run experiment control condition with forced conversation change (everything 3)
python python TatoraTalk.py -commumove -commutalk -control -convoforce

## Stop with Control-C
```


# License

ChatterBot is licensed under the [BSD 3-clause license](https://opensource.org/licenses/BSD-3-Clause).
