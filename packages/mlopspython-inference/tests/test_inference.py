import logging
from pathlib import Path
import pytest

from mlopspython_inference.inference_pillow import Inference

BASE_PATH = Path(__file__).resolve().parent
input_directory = BASE_PATH / "input"


@pytest.mark.skip(reason="Modèle lourd / GPU non requis sur CI. Enlever ce skip si nécessaire.")
def test_inference_runs_with_sample_model_and_image():
    model_path = input_directory / "model" / "final_model.h5"
    image_path = input_directory / "images" / "cat.png"

    assert model_path.is_file(), "Modèle de test manquant"
    assert image_path.is_file(), "Image de test manquante"

    inference = Inference(logging, str(model_path))
    result = inference.execute(str(image_path))

    assert result["prediction"] in {"Cat", "Dog", "Other"}
    assert len(result["values"]) == 3
