import argparse
from pathlib import Path
import mlflow
from label_split_data import DataSplit, LabelSplitDataInput

parser = argparse.ArgumentParser("label_split_data")
parser.add_argument("--labels_input", type=str)
parser.add_argument("--images_input", type=str)
parser.add_argument("--pdfs_input", type=str)
parser.add_argument("--split_images_output", type=str)
parser.add_argument("--split_integration_output", type=str)

# Get arguments from parser
args = parser.parse_args()
labels_input = args.labels_input
images_input = args.images_input
pdfs_input = args.pdfs_input
split_images_output = args.split_images_output
split_integration_output = args.split_integration_output

number_file_by_label = 100
ratio_train: float = 0.7
ratio_test: float = 0.2
number_pdfs_integration = 100

params = {"number_file_by_label": number_file_by_label, "ratio_train": ratio_train, "ratio_test": ratio_test}

mlflow.log_params(params)
labels_files_path = Path(labels_input) / "cats-dogs-others-classification-annotations.json"

label_split_data_input = LabelSplitDataInput(
    labels_files_path,
    Path(images_input),
    Path(pdfs_input),
    Path(split_images_output),
    Path(split_integration_output),
    number_file_by_label,
    number_pdfs_integration,
    ratio_train,
    ratio_test,
)

data_split = DataSplit()
label_split_data_result = data_split.label_split_data(
    label_split_data_input
)
mlflow.log_metric("number_file_train_by_label", label_split_data_result.number_file_train_by_label)
mlflow.log_metric("number_file_test_by_label", label_split_data_result.number_file_test_by_label)
mlflow.log_metric("number_file_evaluate_by_label", label_split_data_result.number_file_evaluate_by_label)
