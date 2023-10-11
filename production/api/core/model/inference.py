from .inference_cv import Inference as InferenceCv
from .inference_pillow import Inference as InferencePillow
from mlopspython_extraction.extraction import extract_images_stream
import mimetypes


def get_mime_type(filepath: str) -> str:
    return mimetypes.guess_type(filepath, strict=False)[0]


class Inference:
    def __init__(self, logging, app_settings):
        self.inference_cv = InferenceCv(logging, app_settings)
        self.inference_pillow = InferencePillow(logging, app_settings)

    def execute(self, file, filename, settings=None):
        print(settings)

        predictions = []

        type = "pillow"
        if "type" in settings:
            type = settings["type"]

        mime_type = get_mime_type(filename)
        if mime_type == "application/pdf":
            stream = file.read()
            for image_stream in extract_images_stream(stream):
                if type == "opencv":
                    prediction = self.inference_cv.execute(image_stream.image_bytes_io, filename, settings)
                else:
                    prediction = self.inference_pillow.execute(image_stream.image_bytes_io, filename, settings)
                predictions.append(prediction)
        elif mime_type in ['image/png', 'image/jpeg', 'image/bmp']:
            if type == "opencv":
                prediction = self.inference_cv.execute(file, filename, settings)
            else:
                prediction = self.inference_pillow.execute(file, filename, settings)
            predictions.append(prediction)

        print("predictions")
        print(predictions)
        return predictions
