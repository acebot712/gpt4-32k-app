from openai import AzureOpenAI
import logging

from settings import api_version, azure_endpoint, api_key, model

class OpenAIClient:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.client = AzureOpenAI(api_version=api_version, azure_endpoint=azure_endpoint, api_key=api_key)
        self.model = model

    def get_response(self, prompt, conversation_history) -> str:
        conversation_history.append((prompt, 'user'))  # consider prompt as the user message

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                # create messages with role based on their origin (assistant or user)
                messages=[{'role': role, 'content': msg} for msg, role in conversation_history])

            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error on Azure OpenAI endpoint. Reason: {e}")
            return "Sorry, I could not process your request."