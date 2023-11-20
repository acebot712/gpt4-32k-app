from openai import AzureOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = AzureOpenAI(api_version=os.environ.get("API_VERSION"),
azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
api_key=os.environ.get("OPENAI_API_KEY"))

model=os.environ.get("MODEL")

 # Your Azure OpenAI resource's endpoint value.

response = client.chat.completions.create(model=model, # The deployment name you chose when you deployed the GPT-3.5-Turbo or GPT-4 model.
messages=[
    {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
    {"role": "user", "content": "Who were the founders of Microsoft?"}
])
print(response.choices[0].message.content)
