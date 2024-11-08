import argparse
from pathlib import Path

from directory_hash import hash_dir
from mlopspython_extraction.extraction import ExtractImages, DataManager
import mlflow

parser = argparse.ArgumentParser("extraction")
parser.add_argument("--trailers_input", type=str)
parser.add_argument("--images_output", type=str)
parser.add_argument("--hash_output", type=str)

args = parser.parse_args()
trailers_input = args.trailers_input
images_output = args.images_output
hash_output = args.hash_output

extract_images = ExtractImages(DataManager())
result = extract_images.extract_images(trailers_input, images_output)

computed_hash = hash_dir(images_output)
with open(str(Path(hash_output) / "hash.txt"), "w") as file:
    file.write(computed_hash)

console_output = f""" 

    number_files_input: {result.number_files_input}
    number_images_output: {result.number_images_output}
    computed_hash: {computed_hash}"""

mlflow.log_metric("number_files_input", result.number_files_input)
mlflow.log_metric("number_images_output", result.number_images_output)
