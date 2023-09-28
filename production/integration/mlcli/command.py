import argparse
from mlcli import run_ml_cli

parser = argparse.ArgumentParser("label_split_data")
parser.add_argument("--integration_input", type=str)
parser.add_argument("--url_input", type=str)
parser.add_argument("--integration_output", type=str)

# Get arguments from parser
args = parser.parse_args()
integration_input = args.integration_input
url_input = args.url_input
integration_output = args.integration_output

with open("./ml-cli.template") as mlcli_file:
    mlcli_template = mlcli_file.read()

run_ml_cli(integration_input, url_input, integration_output, mlcli_template);