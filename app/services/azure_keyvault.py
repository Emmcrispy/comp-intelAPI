import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret(secret_name):
    """Retrieve a secret value from Azure Key Vault."""
    vault_url = f"https://{os.getenv('AZURE_KEY_VAULT_NAME')}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return secret.value

# Example usage (in app factory or config):
# key = get_secret('JwtSecretKey')
# SQLALCHEMY_DATABASE_URI = get_secret('AzureSQLConnectionString')
