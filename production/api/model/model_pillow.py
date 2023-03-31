from pathlib import Path
from mlopspython_inference.model_pillow import Model as ModelPillow

BASE_PATH = Path(__file__).resolve().parent

class Model:
    def __init__(self, logging, app_settings):
        self.logger = logging.getLogger(__name__)
        model_path = (str(BASE_PATH / "cats-dogs-others" / "cats-dogs-others" / 'final_model.h5'))
        self.model = ModelPillow(logging, str(model_path))

    def execute(self, file, filename, settings=None):
        with open(filename, "wb") as stream:
            stream.write(file.getbuffer())

        return self.model.execute(filename)
