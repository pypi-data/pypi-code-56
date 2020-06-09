from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import boto3
import os

AWS_REGION = os.environ["AWS_REGION"]


def _get_appsync_parameters():
    client = boto3.client("ssm", region_name=AWS_REGION)
    url = client.get_parameter(Name="mlops-appsync-url", WithDecryption=True)[
        "Parameter"
    ]["Value"]
    key = client.get_parameter(Name="mlops-appsync-key", WithDecryption=True)[
        "Parameter"
    ]["Value"]
    return url, key


def get_model_hyperparameters(project_id: str, model_id: str) -> dict:
    qry_string = gql(
        """
    query getModels() {
        updateDatasources(input: $input){
            updatedAt
        }
    }
    """
    )
    url, key = _get_appsync_parameters()
    client = Client(
        fetch_schema_from_transport=True,
        transport=RequestsHTTPTransport(
            url=url, headers={"x-api-key": key}, use_json=True,
        ),
    )
    params = {"projectId": project_id, "modelId": model_id}
    return client.execute(qry_string, variable_values=params)
