from pathlib import Path
from ml_cli_azureml_pipeline.run import run_ml_cli_pipeline
import argparse

BASE_PATH = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser("register")
    parser.add_argument(
        "--skip_train_execution",
        action="store_true",
        help=(
            "Do not trigger the execution. "
            "Use this in Azure DevOps when using a server job to trigger"
        ),
    )
    parser.add_argument("--build_id", type=str, default="", help="build id")
    parser.add_argument("--build_tags", type=str, default="", help="add tags")
    parser.add_argument(
        "--config_aml_path",
        type=str,
        default=str(BASE_PATH / "aml" / "config_aml.json"),
        help="configuration azure ml path",
    )
    parser.add_argument("--mlcli_template_json", type=str, default="", help="mlcli template in json")
    parser.add_argument("--datasets_configuration_json", type=str, default="", help="datasets configuration in json")

    args = parser.parse_args()
    config_path = BASE_PATH / "aml/config_env.json"
    mlcli_template_path = BASE_PATH / "aml/ml-cli.template"
    run_ml_cli_pipeline(args, config_path, mlcli_template_path)


if __name__ == "__main__":
    main()
