import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Comp Intel API"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    USE_KEY_VAULT = os.getenv("USE_KEY_VAULT", "false").lower() == "true"

    if USE_KEY_VAULT:
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

        KEY_VAULT_URI = os.getenv("KEY_VAULT_URI")
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KEY_VAULT_URI, credential=credential)

        REDIS_HOST = client.get_secret("RedisHost").value
        REDIS_PORT = int(client.get_secret("RedisPort").value)
        REDIS_PASSWORD = client.get_secret("RedisPassword").value
        DATABASE_URL = client.get_secret("DatabaseUrl").value

    else:
        REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
        REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
        DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()
