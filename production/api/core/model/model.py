#from .model_cv import Model as ModelCv
from .model_pillow import Model as ModelPillow
from mlopspython_extraction.extraction import extract_images_stream


class Model:
	def __init__(self, logging, app_settings):
		#self.model_cv = ModelCv(logging, app_settings)
		self.model_pillow = ModelPillow(logging, app_settings)

	def execute(self, file, filename, settings=None):
		print(settings)
		predictions=[]
		for image_stream in extract_images_stream(file.read()):
			#if settings["type"] == "opencv":
			#	prediction= self.model_cv.execute(file, filename, settings)
			#else:
			prediction= self.model_pillow.execute(image_stream.image_bytes_io, filename, settings)
			predictions.append(prediction)
		print("predictions")
		print(predictions)
		return predictions