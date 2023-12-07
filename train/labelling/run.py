import argparse
import asyncio

from .dataset import download
from .ecotag import create_project, Project, Label, Dataset, ApiInformation, create_dataset

parser = argparse.ArgumentParser("labelling")
parser.add_argument("--jwt_token", type=str)
parser.add_argument("--subscription_id", type=str)
parser.add_argument("--resource_group_name", type=str)
parser.add_argument("--workspace_name", type=str)

args = parser.parse_args()
subscription_id = args.subscription_id
resource_group_name = args.resource_group_name
workspace_name = args.workspace_name
jwt_token = args.jwt_token

async def main():

    dataset_path = download(subscription_id, resource_group_name, workspace_name, 'cats_dogs_others', '1')

    api_url = 'https://axaguildev-ecotag.azurewebsites.net/api/server'
    api_information = ApiInformation(api_url=api_url, jwt_token=jwt_token)

    dataset = Dataset(dataset_name='cats_dogs_others9',
                      dataset_type='Image',
                      team_name='cats_dogs_others',
                      directory=dataset_path,
                      classification='Public')
    await create_dataset(dataset, api_information)

    project = Project(project_name='cats_dogs_others9',
                      dataset_name=dataset.dataset_name,
                      team_name='cats_dogs_others',
                      annotationType='ImageClassifier',
                      labels=[Label(name='cat', color='#FF0000', id="0"), Label(name='dog', color='#00FF00', id="1"), Label(name='other', color='#0000FF', id="2")])

    await create_project(project, api_information)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
