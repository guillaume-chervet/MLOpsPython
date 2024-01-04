import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import random

import numpy as np

random.seed(11)


@dataclass
class LabelSplitDataResult:
    number_file_train_by_label: int
    number_file_test_by_label: int
    number_file_evaluate_by_label: int
    path_results: list[str | Any]
    number_labeled_data: int


def label_split_data(
    input_labels_path: Path,
    input_images_directory: Path,
    input_pdfs_directory: Path,
    output_images_directory: Path,
    output_integration_directory: Path,
    number_image_by_label=3,
    number_pdfs_integration=100,
    ratio_number_train_image: float = 0.4,
    ratio_number_test_image: float = 0.4,
) -> LabelSplitDataResult:
    if ratio_number_test_image + ratio_number_test_image > 1:
        raise Exception("sum of ratio must be inferior or equal to 1")

    Path(output_images_directory).mkdir(parents=True, exist_ok=True)
    Path(output_integration_directory).mkdir(parents=True, exist_ok=True)
    pdfs = [
        p
        for p in Path(input_pdfs_directory).iterdir()
        if p.is_file() and p.suffix == ".pdf"
    ]
    random.shuffle(pdfs)
    images = [
        p
        for p in Path(input_images_directory).iterdir()
        if p.is_file() and p.suffix == ".png"
    ]
    if len(pdfs) > number_pdfs_integration:
        pdfs = pdfs[:number_pdfs_integration]
    pdf_output_directory = output_integration_directory
    pdfs_integration = copy_pdfs_integration(images, pdf_output_directory, pdfs)

    with open(input_labels_path) as json_file:
        label_data = json.load(json_file)

    split_paths = {"cat": [], "dog": [], "other": []}
    labels = ["cat", "dog", "other"]
    split_directory_names = ["train", "test", "evaluate"]
    annotations = label_data["annotations"]
    random.shuffle(annotations)
    for annotation in annotations:
        filename = annotation["fileName"]
        label = annotation["annotation"]["label"]
        if len(split_paths[label]) < number_image_by_label:
            split_paths[label].append(filename)

    number_file_train = int(number_image_by_label * ratio_number_train_image)
    number_file_test = int(number_image_by_label * ratio_number_test_image)
    path_results = []
    for label in labels:
        if number_image_by_label != len(split_paths[label]):
            raise Exception("Not enough files for label " + label)

        splitted = np.split(
            split_paths[label],
            [number_file_train, number_file_test + number_file_train],
        )
        for split_directory_name in split_directory_names:
            labels_directory = (
                output_images_directory / split_directory_name / (label + "s")
            )
            Path(labels_directory).mkdir(parents=True, exist_ok=True)
            for filename in splitted[split_directory_names.index(split_directory_name)]:
                image_pdf_name = filename.split("_")[0]
                if image_pdf_name + ".pdf" in pdfs_integration:
                    continue
                output_filename = label + "_" + filename
                destination_path = labels_directory / output_filename
                source_path = input_images_directory / filename
                destination_path.write_bytes(source_path.read_bytes())
                path_result = (
                    split_directory_name + "/" + label + "s" + "/" + output_filename
                )
                path_results.append(path_result)

    return LabelSplitDataResult(
        number_file_train_by_label=number_file_train,
        number_file_test_by_label=number_file_test,
        number_file_evaluate_by_label=number_image_by_label
        - number_file_train
        - number_file_test,
        path_results=path_results,
        number_labeled_data=len(annotations),
    )


def copy_pdfs_integration(images, pdf_output_directory, pdfs):
    pdfs_integration = []
    for pdf in pdfs:
        pdfs_integration.append(pdf.name)
        (pdf_output_directory / pdf.name).write_bytes(pdf.read_bytes())
    for image_path in images:
        image_pdf_name = image_path.name.split("_")[0]
        if image_pdf_name + ".pdf" not in pdfs_integration:
            continue
        Path(pdf_output_directory / image_pdf_name).mkdir(parents=True, exist_ok=True)
        image_output_path = pdf_output_directory / image_pdf_name / image_path.name
        image_output_path.write_bytes(image_path.read_bytes())
    return pdfs_integration
