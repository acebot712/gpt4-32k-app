import os
from dotenv import load_dotenv

load_dotenv()

api_version = os.environ.get("API_VERSION")
azure_endpoint = os.environ.get("AZURE_ENDPOINT")
api_key = os.environ.get("OPENAI_API_KEY")
model = os.environ.get("MODEL")