import json
import logging
import unittest
from pathlib import Path

from model_pillow import Model

BASE_PATH = Path(__file__).resolve().parent
output_directory = BASE_PATH / "output"
input_directory = BASE_PATH / "input"

class EvaluateTest(unittest.TestCase):

    def test_something(self):
        output_directory.mkdir(parents=True, exist_ok=True)
        model = Model(logging, str(input_directory / "final_model.h5"))

        results = []
        cats_directory = input_directory / "evaluate"
        for path in cats_directory.glob("**/*"):
            if path.is_dir():
                continue
            model_result = model.execute(str(path))

            prediction = model_result["prediction"]
            prediction_truth = path.parent.name.lower().replace("s", "")
            result = { "filepath": path.name,
                       "ok": prediction_truth == prediction.lower(),
                       "prediction": prediction,
                       "values": model_result["values"] }
            results.append(result)

        with open( output_directory / "predictions.json", 'w') as file_stream:
            json.dump(results, file_stream, indent=4)
        

if __name__ == '__main__':
    unittest.main()
