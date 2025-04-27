from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os

def authenticate_text_analytics():
    key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
    endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client

def extract_key_phrases(text_list):
    """Extract key phrases from a list of texts using Azure AI Language."""
    client = authenticate_text_analytics()
    try:
        response = client.extract_key_phrases(documents=text_list)
        return [res.key_phrases if not res.is_error else [] for res in response]
    except Exception as e:
        print(f"Azure AI error: {e}")
        return []
