import io
from pathlib import Path
from mlopspython_inference.inference_pillow import Inference as InferencePillow, ModelLoader

BASE_PATH = Path(__file__).resolve().parent

class Inference:
    def __init__(self, logging, app_settings, model_loader: ModelLoader):
        self.logger = logging.getLogger(__name__)
        model_path = (str(BASE_PATH / 'final_model.h5'))
        self.inference = InferencePillow(logging, ModelLoader(str(model_path)))

    def execute(self, file, filename, settings=None):
        return self.inference.execute(io.BytesIO(file.read()))
