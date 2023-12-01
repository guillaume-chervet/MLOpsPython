import asyncio

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from .ecotag import create_project, Project, Label, Dataset, ApiInformation, create_dataset

def download_dataset():
    ml_client = MLClient.from_config(credential=DefaultAzureCredential())
    data_asset = ml_client.data.get("cats-dogs-others-extraction", version="1")

    path = {
        'folder': data_asset.path
    }
    return path["folder"]
async def main():

    api_url = 'https://axaguildev-ecotag.azurewebsites.net/api/server'
    jwt_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkMyNTJGOUNBQjc3Q0MxNTQwNTBFMTg1NTk5MjJCMTJGIiwidHlwIjoiYXQrand0In0.eyJpc3MiOiJodHRwczovL2RlbW8uZHVlbmRlc29mdHdhcmUuY29tIiwibmJmIjoxNzAxNDQ2MTM3LCJpYXQiOjE3MDE0NDYxMzcsImV4cCI6MTcwMTQ0OTczNywiYXVkIjoiYXBpIiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsImVtYWlsIiwiYXBpIl0sImFtciI6WyJwd2QiXSwiY2xpZW50X2lkIjoiaW50ZXJhY3RpdmUucHVibGljIiwic3ViIjoiMiIsImF1dGhfdGltZSI6MTcwMTQ0NTkxMSwiaWRwIjoibG9jYWwiLCJuYW1lIjoiQm9iIFNtaXRoIiwiZW1haWwiOiJCb2JTbWl0aEBlbWFpbC5jb20iLCJzaWQiOiJGNTJBNDVBNDJEQUZENTlCMDQ5NkFDRTJBOUEzMTk0QiIsImp0aSI6IkZCRDExNTAyRUEwMjkzQzhFMkJDQ0ZFQ0I4Mjc3M0JDIn0.pgIhB6_VvoEAtBXR8LnSlPnoILkk1kocbA2Xst6MH5WtPpySx_sheUkNPnyaJ0iNMX33wNusXK6mF1Pd1HEhEwrwMg-ixuUM-5sj0zTZ5kqR8GyMBKNy8QG_DgqrXxTDo1LH5ppEZbWWbWeLvccU1LJlMWbDEbEGohj46WwV_GoHhGtMH1LD6DVa3Ds3xDCVVlzKcBTOMNwQcqWo5HfNiFBqBBjxqbRhsROl88Irhki34h-nUCc8hITia3hn7i8jjtNon6Nkh5wHagszd44TSZygPZpY2ID3185-LeQEImu3At6ySn1k5MGd5pDMw42XcZNrIxEUzyCmqxKVT880Tw'
    api_information = ApiInformation(api_url=api_url, jwt_token=jwt_token)

    dataset = Dataset(dataset_name='cats_dogs_others9',
                      dataset_type='Image',
                      team_name='cats_dogs_others',
                      directory=path.folder,
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
