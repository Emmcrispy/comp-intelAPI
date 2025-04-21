import os
from dotenv import load_dotenv

# Load local .env for local development
load_dotenv()
print("Loaded DATABASE_URL from .env:", os.getenv("DATABASE_URL"))
class Settings:
    APP_NAME = "Comp Intel API"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    USE_KEY_VAULT = os.getenv("USE_KEY_VAULT", "false").lower() == "true"

    def __init__(self):
        if self.USE_KEY_VAULT:
            self.load_from_key_vault()
        else:
            self.load_from_env()

    def load_from_key_vault(self):
        try:
            from azure.identity import DefaultAzureCredential
            from azure.keyvault.secrets import SecretClient

            key_vault_uri = os.getenv("KEY_VAULT_URI")
            if not key_vault_uri:
                raise ValueError("KEY_VAULT_URI is not set.")

            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=key_vault_uri, credential=credential)

            self.REDIS_HOST = client.get_secret("RedisHost").value
            self.REDIS_PORT = int(client.get_secret("RedisPort").value)
            self.REDIS_PASSWORD = client.get_secret("RedisPassword").value
            self.DATABASE_URL = client.get_secret("DatabaseUrl").value

        except Exception as e:
            raise RuntimeError(f"Failed to load secrets from Azure Key Vault: {e}")

    def load_from_env(self):
        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
        self.REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
        self.DATABASE_URL = os.getenv("DATABASE_URL", "mssql+pyodbc://localhost/SQLEXPRESS?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes")

settings = Settings()
