from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os

async def process_job_description(description):
    credential = AzureKeyCredential(os.getenv("AZURE_NLP_KEY"))
    client = TextAnalyticsClient(endpoint=os.getenv("AZURE_NLP_ENDPOINT"), credential=credential)
    response = client.extract_key_phrases([description])[0]
    return response.key_phrases
