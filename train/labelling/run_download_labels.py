import argparse
import asyncio
from pathlib import Path

from ecotag import (
    ApiInformation,
    download_annotations,
)
from requests_oauth2client import OAuth2Client

parser = argparse.ArgumentParser("download_labels")
parser.add_argument("--jwt_token", type=str, default="")
parser.add_argument("--project_name", type=str)
parser.add_argument("--api_url", type=str)

args = parser.parse_args()
jwt_token = args.jwt_token
project_name = args.project_name
api_url = args.api_url

if jwt_token == "":
    oauth2client = OAuth2Client(
        token_endpoint="https://demo.duendesoftware.com/connect/token",
        auth=("m2m", "secret"),
    )
    token = oauth2client.client_credentials(scope="api")
    jwt_token = token["access_token"]

async def main():
    base_path = Path(__file__).resolve().parent
    dataset_path = base_path / "labels"
    filename = "cats-dogs-others-classification-annotations.json"
    dataset_path.mkdir(exist_ok=True)

    api_information = ApiInformation(api_url=api_url, jwt_token=jwt_token)
    await download_annotations(
        api_information, project_name, str(dataset_path), filename
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
