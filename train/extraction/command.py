import argparse
from mlopspython_extraction.extraction import extract_images
import mlflow

from directory_hash import hash_dir

parser = argparse.ArgumentParser("extraction")
parser.add_argument("--pdfs_input", type=str)
parser.add_argument("--images_output", type=str)
parser.add_argument("--hash_output", type=str)

args = parser.parse_args()
pdfs_input = args.pdfs_input
images_output = args.images_output
hash_output = args.hash_output

result = extract_images(pdfs_input, images_output)
computed_hash = hash_dir(images_output)
with open(str(hash_output / "hash.txt"), "w") as file:
    file.write(computed_hash)

mlflow.log_metric("hash", computed_hash)
mlflow.log_metric("number_files_input", result.number_files_input)
mlflow.log_metric("number_images_output", result.number_images_output)