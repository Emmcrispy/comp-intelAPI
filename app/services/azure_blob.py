from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os

def get_blob_service_client():
    """Create Azure BlobServiceClient using DefaultAzureCredential."""
    account_url = f"https://{os.getenv('AZURE_STORAGE_ACCOUNT_NAME')}.blob.core.windows.net"
    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url=account_url, credential=credential)

def upload_file(container_name, file_path, blob_name):
    """Upload a file to Azure Blob Storage (stub)."""
    client = get_blob_service_client()
    container_client = client.get_container_client(container_name)
    with open(file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data)
    return True
