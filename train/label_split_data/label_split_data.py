import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass
class LabelSplitDataResult:
    number_file_train_by_label: int
    number_file_test_by_label: int
    number_file_evaluate_by_label: int
    path_results: list[str | Any]
    number_labeled_data: int


def label_split_data(input_labels_path: Path,
                     input_images_directory: Path,
                     output_directory: Path,
                     number_file_by_label=3,
                     ratio_train: float = 0.4,
                     ratio_test: float = 0.4) -> LabelSplitDataResult:

    if ratio_test + ratio_test > 1:
        raise Exception("sum of ratio must be inferior or equal to 1")

    Path(output_directory).mkdir(parents=True, exist_ok=True)
    with open(input_labels_path) as json_file:
        label_data = json.load(json_file)

    split_paths = {"cat": [], "dog": [], "other": []}
    labels = ["cat", "dog", "other"]
    split_directory_names = ["train", "test", "evaluate"]
    annotations = label_data["annotations"]
    for annotation in annotations:
        filename = annotation["fileName"]
        label = annotation["annotation"]["label"]
        if len(split_paths[label]) < number_file_by_label:
            split_paths[label].append(filename)

    number_file_train = int(number_file_by_label * ratio_train)
    number_file_test = int(number_file_by_label * ratio_test)
    path_results = []
    for label in labels:
        if number_file_by_label != len(split_paths[label]):
            raise Exception("Not enough files for label " + label)

        splitted = np.split(split_paths[label], [number_file_train, number_file_test + number_file_train])
        for split_directory_name in split_directory_names:
            labels_directory = output_directory / split_directory_name / (label + "s")
            Path(labels_directory).mkdir(parents=True, exist_ok=True)
            for filename in splitted[split_directory_names.index(split_directory_name)]:
                output_filename = label + "_" + filename
                destination_path = labels_directory / output_filename
                source_path = input_images_directory / filename
                destination_path.write_bytes(source_path.read_bytes())
                path_result = split_directory_name + "/" + label + "s" + "/" + output_filename
                path_results.append(path_result)

    return LabelSplitDataResult(
        number_file_train_by_label=number_file_train,
        number_file_test_by_label=number_file_test,
        number_file_evaluate_by_label=number_file_by_label - number_file_train - number_file_test,
        path_results=path_results,
        number_labeled_data=len(annotations))
