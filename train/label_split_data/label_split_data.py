import json
from abc import abstractmethod, ABC
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List
import random

import numpy as np


class IDataRandom(ABC):
    @abstractmethod
    def shuffle(self, x: list) -> None:
        pass

    @abstractmethod
    def seed(self, seed: int) -> None:
        pass


class IDataManager(ABC):

    @abstractmethod
    def load_json(self, json_path: Path) -> Any:
        pass

    @abstractmethod
    def list_files(self, directory_path: Path, suffix: str) -> List[Path]:
        pass

    @abstractmethod
    def copy_file(self, file_path: Path, to_file_path: Path) -> None:
        pass

    @abstractmethod
    def create_directory(self, directory_path: Path) -> None:
        pass


class DataRandom(IDataRandom):
    def shuffle(self, x: list) -> None:
        random.shuffle(x)

    def seed(self, seed: int) -> None:
        random.seed(seed)


class DataManager(IDataManager):
    def load_json(self, json_path: Path) -> Any:
        with open(json_path) as json_file:
            return json.load(json_file)

    def list_files(self, directory_path: Path, suffix: str) -> List[Path]:
        return [p for p in directory_path.iterdir() if p.is_file() and p.suffix == suffix]

    def copy_file(self, source_path: Path, destination_path: Path) -> None:
        destination_path.write_bytes(source_path.read_bytes())

    def create_directory(self, directory_path: Path) -> None:
        directory_path.mkdir(parents=True, exist_ok=True)


@dataclass
class LabelSplitDataResult:
    number_file_train_by_label: int
    number_file_test_by_label: int
    number_file_evaluate_by_label: int
    number_labeled_data: int


@dataclass
class LabelSplitDataInput:
    input_labels_path: Path
    input_images_directory: Path
    input_trailers_directory: Path
    output_images_directory: Path
    output_integration_directory: Path
    number_image_by_label: int = 3
    number_pdfs_integration: int = 100
    ratio_number_train_image: float = 0.4
    ratio_number_test_image: float = 0.4


class DataSplit:

    def __init__(self, data_random: IDataRandom = DataRandom(), data_manager: IDataManager = DataManager()):
        self.data_random = data_random
        self.data_manager = data_manager

    def label_split_data(
            self,
            input: LabelSplitDataInput
    ) -> LabelSplitDataResult:
        input_labels_path = input.input_labels_path
        input_images_directory = input.input_images_directory
        input_trailers_directory = input.input_trailers_directory
        output_images_directory = input.output_images_directory
        output_integration_directory = input.output_integration_directory
        number_image_by_label = input.number_image_by_label
        number_pdfs_integration = input.number_pdfs_integration
        ratio_number_train_image = input.ratio_number_train_image
        ratio_number_test_image = input.ratio_number_test_image

        self.data_random.seed(11)
        if ratio_number_test_image + ratio_number_test_image > 1:
            raise Exception("sum of ratio must be inferior or equal to 1")

        copy_trailers_integration_input = CopyPdfsIntegrationInput(input_images_directory,
                                                               input_trailers_directory,
                                                               output_integration_directory,
                                                               number_pdfs_integration)

        trailers_integration = copy_trailers_integration(self.data_random, self.data_manager, copy_trailers_integration_input)

        split_copy_data_input = SplitCopyDataInput(input_images_directory, input_labels_path, number_image_by_label,
                                                   output_images_directory, trailers_integration,
                                                   ratio_number_test_image, ratio_number_train_image)

        return split_copy_data(self.data_random,
                               self.data_manager,
                               split_copy_data_input)


@dataclass
class SplitCopyDataInput:
    input_images_directory: Path
    input_labels_path: Path
    number_image_by_label: int
    output_images_directory: Path
    trailers_integration: [str]
    ratio_number_test_image: float
    ratio_number_train_image: float


def split_copy_data(data_random: IDataRandom,
                    data_manager: IDataManager,
                    input: SplitCopyDataInput) -> LabelSplitDataResult:
    input_images_directory = input.input_images_directory
    input_labels_path = input.input_labels_path
    number_image_by_label = input.number_image_by_label
    output_images_directory = input.output_images_directory
    trailers_integration = input.trailers_integration
    ratio_number_test_image = input.ratio_number_test_image
    ratio_number_train_image = input.ratio_number_train_image

    data_manager.create_directory(output_images_directory)
    label_data = data_manager.load_json(input_labels_path)
    split_paths = {"arme": [], "agression": [], "alcool": [], "tout public": []}
    labels = ["arme", "agression", "alcool", "tout public"]
    split_directory_names = ["train", "test", "evaluate"]
    annotations = label_data["annotations"]
    data_random.shuffle(annotations)
    for annotation in annotations:
        filename = annotation["fileName"]
        label = annotation["annotation"]["label"]
        if len(split_paths[label]) < number_image_by_label:
            split_paths[label].append(filename)
    number_file_train = int(number_image_by_label * ratio_number_train_image)
    number_file_test = int(number_image_by_label * ratio_number_test_image)
    for label in labels:
        if number_image_by_label > len(split_paths[label]):
            raise Exception("Not enough files for label " + label)

        splitted = np.split(
            split_paths[label],
            [number_file_train, number_file_test + number_file_train],
        )
        for split_directory_name in split_directory_names:
            labels_directory = (
                    output_images_directory / split_directory_name / (label + "s")
            )
            data_manager.create_directory(labels_directory)
            for filename in splitted[split_directory_names.index(split_directory_name)]:
                image_trailer_name = filename.split("_")[0]
                if image_trailer_name + ".mp4" in trailers_integration:
                    continue
                output_filename = label + "_" + filename
                destination_path = labels_directory / output_filename
                source_path = input_images_directory / filename
                data_manager.copy_file(source_path, destination_path)
                path_result = (
                        split_directory_name + "/" + label + "s" + "/" + output_filename
                )
    return LabelSplitDataResult(
        number_file_train_by_label=number_file_train,
        number_file_test_by_label=number_file_test,
        number_file_evaluate_by_label=number_image_by_label
                                      - number_file_train
                                      - number_file_test,
        number_labeled_data=len(annotations),
    )


@dataclass
class CopyPdfsIntegrationInput:
    input_images_directory: Path
    input_trailers_directory: Path
    output_integration_directory: Path
    number_trailers_integration: int


def copy_trailers_integration(data_random: IDataRandom,
                          data_manager: IDataManager,
                          input: CopyPdfsIntegrationInput):
    input_images_directory = input.input_images_directory
    input_trailers_directory = input.input_trailers_directory
    output_integration_directory = input.output_integration_directory
    number_trailers_integration = input.number_trailers_integration

    data_manager.create_directory(output_integration_directory)
    trailers = data_manager.list_files(input_trailers_directory, ".mp4")
    data_random.shuffle(trailers)

    images = data_manager.list_files(input_images_directory, ".jpg")

    if len(trailers) > number_trailers_integration:
        trailers = trailers[:number_trailers_integration]
    trailer_output_directory = output_integration_directory

    trailers_integration = []
    for trailer in trailers:
        trailers_integration.append(trailer.name)
        data_manager.copy_file(trailer, trailer_output_directory / trailer.name)
    for image_path in images:
        image_trailer_name = image_path.name.split("_")[0]
        if image_trailer_name + ".mp4" not in trailers_integration:
            continue
        data_manager.create_directory(trailer_output_directory / image_trailer_name)
        image_output_path = trailer_output_directory / image_trailer_name / image_path.name
        data_manager.copy_file(image_path, image_output_path)
    return trailers_integration
