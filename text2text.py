from openai import AzureOpenAI
import logging
import json

from settings import api_version, azure_endpoint, api_key, model


def get_current_weather(location, format="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps(
            {"location": "San Francisco", "temperature": "72", "unit": "fahrenheit"}
        )
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})


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
                        "name": "get_current_weather",
                        "description": "Get the current weather",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA",
                                },
                                "format": {
                                    "type": "string",
                                    "enum": ["celsius", "fahrenheit"],
                                    "description": "The temperature unit to use. Infer this from the users location.",
                                },
                            },
                            "required": ["location", "format"],
                        },
                    }
                ],
                function_call="auto",
            )

            return response.choices[0].message
        except Exception as e:
            self.logger.error(f"Error on Azure OpenAI endpoint. Reason: {e}")
            return "Sorry, I could not process your request."


if __name__ == "__main__":
    client = OpenAIClient()
    response_message = client.get_response_raw(
        "What's the weather like in San Francisco, Tokyo, and Paris?"
    )
    print(response_message.function_call)
    function_name = response_message.function_call.name
    function_args = json.loads(response_message.function_call.arguments)
    print(f"{function_name=}")
    print(f"{function_args=}")
    print(get_current_weather(**function_args))
