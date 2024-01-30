import argparse
import asyncio
from pathlib import Path

from ecotag_sdk.ecotag import (
    ApiInformation,
    download_annotations,
    get_access_token,
)


parser = argparse.ArgumentParser("download_labels")
parser.add_argument("--access_token", type=str, default="")
parser.add_argument(
    "--project_name", type=str, default="cats_dogs_others_classification"
)
parser.add_argument(
    "--api_url",
    type=str,
    default="https://axaguildev-ecotag.azurewebsites.net/api/server",
)
parser.add_argument(
    "--token_endpoint",
    type=str,
    default="https://demo.duendesoftware.com/connect/token",
)
parser.add_argument("--client_id", type=str, default="m2m")
parser.add_argument("--client_secret", type=str, default="secret")

args = parser.parse_args()
access_token = args.access_token
project_name = args.project_name
api_url = args.api_url
token_endpoint = args.token_endpoint
client_id = args.client_id
client_secret = args.client_secret

if access_token == "":
    access_token = get_access_token(token_endpoint, client_id, client_secret)


async def main():
    base_path = Path(__file__).resolve().parent
    dataset_path = base_path / "labels"
    filename = "cats-dogs-others-classification-annotations.json"
    dataset_path.mkdir(exist_ok=True)

    api_information = ApiInformation(api_url=api_url, access_token=access_token)
    await download_annotations(
        api_information, project_name, str(dataset_path), filename
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
