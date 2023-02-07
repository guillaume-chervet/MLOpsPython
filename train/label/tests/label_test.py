import json
import shutil
import unittest
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent


class LabelTest(unittest.TestCase):
    output_directory = BASE_PATH / "output" / "labelled_images"
    input_directory = BASE_PATH / "input"
    input_images_directory = input_directory / "images"
    input_labels_path = input_directory / "labels" / "labels.json"

    def tearDown(self):
        if self.output_directory.is_dir():
            shutil.rmtree(str(self.output_directory))

    def test_label(self):
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)
        with open(self.input_labels_path) as json_file:
            data = json.load(json_file)

        for annotation in data["annotations"]:
            filename = annotation["fileName"]
            label = annotation["annotation"]["label"]
            output_filename = label + "_" + filename
            dest = self.output_directory / output_filename
            src = self.input_images_directory / filename
            dest.write_bytes(src.read_bytes())

        expected = ['cat_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page1_index0.png',
                    'cat_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page3_index0.png',
                    'dog_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page2_index0.png',
                    'dog_0a2bc279-8a6b-49fd-9857-d047351cd5e9_page4_index0.png',
                    'other_0a0e5d35-ef01-4239-af60-81f2357a6ab9_page0_index0.png',
                    'other_0a0e5d35-ef01-4239-af60-81f2357a6ab9_page1_index0.png']
        images = [p for p in Path(self.output_directory).iterdir() if p.is_file()]
        for image_path in images:
            self.assertIn(image_path.name, expected)

if __name__ == '__main__':
    unittest.main()
