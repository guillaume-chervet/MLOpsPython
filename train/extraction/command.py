import argparse
from pathlib import Path

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
with open(str(Path(hash_output) / "hash.txt"), "w") as file:
    file.write(computed_hash)

console_output = f""" 
    number_files_input: {result.number_files_input}
    number_images_output: {result.number_images_output}
    computed_hash: {computed_hash}
"""
mlflow.log_metric("number_files_input", result.number_files_input)
mlflow.log_metric("number_images_output", result.number_images_output)