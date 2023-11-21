from openai import AzureOpenAI
import logging
import json
from search import search_ddg

from settings import api_version, azure_endpoint, api_key, model


class OpenAIClient:
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.client = AzureOpenAI(
            api_version=api_version, azure_endpoint=azure_endpoint, api_key=api_key
        )
        self.model = model

    def get_response(self, prompt, conversation_history) -> str:
        conversation_history.append(
            (prompt, "user")
        )  # consider prompt as the user message

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                # create messages with role based on their origin (assistant or user)
                messages=[
                    {"role": role, "content": msg} for msg, role in conversation_history
                ],
            )

            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error on Azure OpenAI endpoint. Reason: {e}")
            return "Sorry, I could not process your request."

    def get_response_raw(self, prompt) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                # create messages with role based on their origin (assistant or user)
                messages=[
                    {
                        "role": "system",
                        "content": "Assistant is a large language model trained by OpenAI.",
                    },
                    {"role": "user", "content": prompt},
                ],
                functions=[
                    {
                        "name": "search_ddg",
                        "description": "Searches for a query on DuckDuckGo and returns the abstract from the JSON response",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The search query, e.g. Python Programming",
                                }
                            },
                            "required": ["query"],
                        },
                    }
                ],
                function_call="auto",
            )
            response_message = response.choices[0].message

            if response_message.function_call:
                print("HERE")
                function_name = response_message.function_call.name
                function_args = json.loads(response_message.function_call.arguments)
                return globals()[function_name](**function_args)
            
            print("NOW HERE")

            return response.choices[0].message
        except Exception as e:
            self.logger.error(f"Error on Azure OpenAI endpoint. Reason: {e}")
            return "Sorry, I could not process your request."


if __name__ == "__main__":
    client = OpenAIClient()
    response = client.get_response_raw(
        "Python Programming"
    )
    print(response)
