from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os

import tensorflow as tf

import configuration
import inference_wrapper
from inference_utils import caption_generator
from inference_utils import vocabulary


class ImageCaptioner():
	def __init__(self, model_path, vocab_file):
		self.model_path = model_path
		self.vocab_file = vocab_file

		# Build the inference graph.
		self.g = tf.Graph()
		with self.g.as_default():
			self.model = inference_wrapper.InferenceWrapper()
			self.restore_fn = self.model.build_graph_from_config(configuration.ModelConfig(), self.model_path)
		self.g.finalize()

		# Create the vocabulary.
		self.vocab = vocabulary.Vocabulary(self.vocab_file)

		self.openSession()

	def openSession(self):
		self.sess = tf.Session(graph=self.g)
		self.restore_fn(self.sess)
		self.generator = caption_generator.CaptionGenerator(self.model, self.vocab)

	def closeSession(self):
		self.sess.close()

	def getCaption(self, img_filename):
		with tf.gfile.GFile(img_filename, "r") as f:
			image = f.read()
		captions = self.generator.beam_search(self.sess, image)
		print("Captions for image %s:" % os.path.basename(img_filename))
		for i, caption in enumerate(captions):
			# Ignore begin and end words.
			sentence = [self.vocab.id_to_word(w) for w in caption.sentence[1:-1]]
			sentence = " ".join(sentence)
			print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))


if __name__ == "__main__":
	IC = ImageCaptioner("/home/sean/Desktop/OUIRL-ChatBot/chatterbot/imgcaption/pretrained_model/model.ckpt-2000000",\
		"/home/sean/Desktop/OUIRL-ChatBot/chatterbot/imgcaption/pretrained_model/word_counts.txt")
	IC.openSession()
	IC.getCaption("/home/sean/Downloads/tv-on-table.jpg")
	IC.closeSession()