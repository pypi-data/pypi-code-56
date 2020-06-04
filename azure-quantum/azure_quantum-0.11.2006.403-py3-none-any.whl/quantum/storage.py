##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import io
import logging
from typing import Any

from azure.storage.blob import BlobServiceClient, ContainerClient, BlobSasPermissions, ContentSettings, generate_blob_sas, generate_container_sas
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def create_container(connection_string: str, container_name: str) -> ContainerClient:
    """
    Creates and initialize a container; returns the client needed to access it.
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    logger.info(f"Initializing storage client for account: '{blob_service_client.account_name}'")

    container_client = blob_service_client.get_container_client(container_name)
    try:
        container_client.get_container_properties()
        logger.debug(f"  - uploading to existing container")
    except:
        logger.debug(f"  - uploading to **new** container: {container_client.container_name}")
        container_client.create_container()
    return container_client

def get_container_uri(connection_string: str, container_name: str) -> str:
    """
    Creates and initialize a container; returns a URI with a SAS read/write token to access it.
    """
    container = create_container(connection_string, container_name)
    logger.info(f"Creating SAS token for container '{container_name}' on account: '{container.account_name}'")

    sas_token = generate_container_sas(
        container.account_name,
        container.container_name,
        account_key=container.credential.account_key,
        permission=BlobSasPermissions(read=True, add=True, write=True, create=True),
        expiry= datetime.utcnow() + timedelta(days=14)
    )

    uri = container.url + "?" + sas_token
    logger.debug(f"  - container url: '{uri}'.")
    return uri


def upload_blob(connection_string: str, container_name: str, blob_name: str, content_type:str, content_encoding:str, data: Any) -> str:
    """
    Uploads the given data to a blob record. If a blob with the given name already exist, it throws an error.

    Returns a uri with a SAS token to access the newly created blob.
    """
    container = create_container(connection_string, container_name)
    logger.info(f"Uploading blob '{blob_name}' to container '{container_name}' on account: '{container.account_name}'")

    content_settings = ContentSettings(content_type=content_type, content_encoding=content_encoding)
    blob = container.get_blob_client(blob_name)
    blob.upload_blob(data, content_settings=content_settings)
    logger.debug(f"  - blob '{blob_name}' uploaded. generating sas token.")

    sas_token = generate_blob_sas(
        blob.account_name,
        blob.container_name,
        blob.blob_name,
        account_key=blob.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry= datetime.utcnow() + timedelta(days=14)
    )

    uri = blob.url + "?" + sas_token
    logger.debug(f"  - blob access url: '{uri}'.")

    return uri
    

def download_blob(container_url: str, blob_name: str) -> Any:
    """
    Downloads the given blob from the container.
    """
    container = ContainerClient.from_container_url(container_url)
    logger.info(f"Downloding blob '{blob_name}' from container '{container.container_name}' on account: '{container.account_name}'")

    blob = container.get_blob_client(blob_name)
    response = blob.download_blob().readall()
    logger.debug(response)

    return response

