# Image Captioning - im2txt

This is an experimental fork upon the [Show and Tell Neural Network Model](https://github.com/tensorflow/models/tree/master/im2txt). The aim is to use this model to help introduce visual stimuli into chatterbot conversation.

- Removed Bazel compilation routine
- ```train.py``` and ```evaluate.py``` not changed, so not sure if they work
- Pretrained models from [KranthiGV](https://github.com/KranthiGV/Pretrained-show-and-Tell-model)

## Setup Overview

### Install Required Packages
First ensure that you have installed the following required packages (its suggest that you use anaconda2 to conda install tensorflow, numpy, and nltk):

* **TensorFlow** 1.0 or greater ([instructions](https://www.tensorflow.org/install/))
* **NumPy** ([instructions](http://www.scipy.org/install.html))
* **Natural Language Toolkit (NLTK)**:
    * First install NLTK ([instructions](http://www.nltk.org/install.html))
    * Then install the NLTK data ([instructions](http://www.nltk.org/data.html))
* **OpenCV**
    * Must have OpenCV version with ffmpeg enabled, or else ```cv2.VideoCapture``` command will not work
    * Due to above problem, this is very difficult to solve and use. Still trying to figure out how to make it work reliably
* **Scikit-Video**
	* Used as a more reliable way to read video files as OpenCV has problems working on Linux
	* Use ```pip install scikit-video``` and ```sudo apt-get install libav-tools``` in Ubuntu. libav is needed for ```skvideo.io.VideoCapture(filename)``` to work without giving "No such file or directory" error

### Download Pretrained Data

Download the [2M iterations finetuned checkpoint file](https://drive.google.com/file/d/0B3laN3vvvSD2T1RPeDA5djJ6bFE/view?usp=sharing) into pretrained_model folder | [Released under MIT License](https://github.com/KranthiGV/Pretrained-Show-and-Tell-model/blob/master/LICENSE)

### Running

For example captioning of a single image, check ```im2txt/get_imgcaption.py```. Change ImageCaptioner instantiation parameters to the relevant pretrained_model paths, then run:

```
python get_imgcaption.py
```
