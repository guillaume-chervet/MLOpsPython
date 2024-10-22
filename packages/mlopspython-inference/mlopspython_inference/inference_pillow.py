from abc import ABC
from io import BytesIO

import numpy as np
from PIL import Image
from keras.models import load_model
from pathlib import Path


def load_image(filename: str | BytesIO):
    # Open the image
    if isinstance(filename, BytesIO):
        img = Image.open(filename)
    else:
        img = Image.open(Path(filename))

    # Resize the image to 224x224
    img = img.resize((224, 224))

    # Convert image to NumPy array (shape: height x width x channels)
    img_array = np.array(img)

    # Ensure it's 3 channels (RGB)
    if img_array.shape[-1] != 3:
        img_array = img_array[:, :, :3]  # Convert to RGB if it has an alpha channel

    # Convert the array to float32 and reshape into (1, 224, 224, 3)
    img_array = img_array.astype('float32')
    img_array = img_array.reshape((1, 224, 224, 3))

    # Center pixel values (subtract mean pixel values)
    img_array -= [123.68, 116.779, 103.939]

    return img_array


BASE_PATH = Path(__file__).resolve().parent

class IModel(ABC):
    def predict(self, img: np.ndarray) -> np.ndarray:
        pass

class Model(IModel):
    def __init__(self, model_path: str):
        self.model = load_model(model_path)

    def predict(self, img: np.ndarray) -> np.ndarray:
        return self.model.predict(img)

class ModelMock(IModel):
    def predict(self, img: np.ndarray) -> np.ndarray:
        return np.array([[0.1, 0.2, 0.7]])


class Inference:
    def __init__(self, logging, model: IModel):
        self.logger = logging.getLogger(__name__)
        self.model = model

    def execute(self, filepath:str|BytesIO):
        img = load_image(filepath)
        result = self.model.predict(img)
        values = [float(result[0][0]), float(result[0][1]), float(result[0][2])]
        switcher = ['Cat', 'Dog', 'Other']
        prediction = np.argmax(result[0])
        return {"prediction": switcher[prediction], "values": values}
