from keras.models import load_model
from pathlib import Path

import numpy as np
import cv2

# load and prepare the image
def load_image(file):
	# load the image
	img_array = np.asarray(bytearray(file), dtype=np.uint8)
	local_file = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
	img = cv2.resize(local_file, (224, 224), interpolation=cv2.INTER_CUBIC)
	# convert to array
	# Numpy array
	np_image_data = np.asarray(img)
	# maybe insert float convertion here - see edit remark!
	np_final = np.expand_dims(np_image_data, axis=0)
	# reshape into a single sample with 3 channels
	img = np_final.reshape(1, 224, 224, 3)
	# center pixel data
	img = img.astype('float32')
	img = img - [123.68, 116.779, 103.939]
	return img

BASE_PATH = Path(__file__).resolve().parent

class Inference:
	def __init__(self, logging, app_settings):
		self.logger = logging.getLogger(__name__)
		model_path = (str(BASE_PATH / 'final_model.h5'))
		self.model = load_model(model_path)

	def execute(self, file, filename, settings=None):
		img = load_image(file.read())
		# predict the class
		result = self.model.predict(img)
		values = [float(result[0][0]), float(result[0][1]), float(result[0][2])]
		print("prediction_values")
		switcher = ['Cat', 'Dog', 'Other']
		prediction = np.argmax(result[0])
		return { "prediction": switcher[prediction], "values": values }