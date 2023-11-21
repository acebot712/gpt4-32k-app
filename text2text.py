import logging
import json
from typing import List, Tuple
from openai import AzureOpenAI
from settings import api_version, azure_endpoint, api_key, model
from search import search_ddg
from openai.types.chat.chat_completion_message import FunctionCall

logger = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(self) -> None:
        self.client = self._create_azure_client()

    @staticmethod
    def _create_azure_client() -> AzureOpenAI:
        return AzureOpenAI(
            api_version=api_version, azure_endpoint=azure_endpoint, api_key=api_key
        )

    @staticmethod
    def get_messages_content(conversation_history: List[Tuple[str, str]]) -> List[dict]:
        """
        Transforms the conversation history into a structure understandable by the OpenAI API

        :param conversation_history: List of tuples where each tuple is a message and its author (message, author)
        :return: a list of dictionaries with the role and content of each message
        """
        try:
            return [
                {"role": role, "content": msg} for msg, role in conversation_history
            ]
        except Exception as e:
            logger.error(f"Error when getting message content. Exception: {e}")
            return []

    def execute_function(self, function_call) -> str:
        function_name = function_call.name
        function_args = json.loads(function_call.arguments)

        # Check if function name exists in globals and is callable
        func = globals().get(function_name)
        if not func or not callable(func):
            raise ValueError(
                f"Function '{function_name}' does not exist or is not callable."
            )

        return func(**function_args)

    def get_response(
        self, prompt: str, conversation_history: List[Tuple[str, str]]
    ) -> str:
        """
        Generates a response from the OpenAI API based on the given prompt and conversation history

        :param prompt: The prompt to send to the OpenAI API
        :param conversation_history: The history of the conversation up to this point
        :return: The response from the OpenAI API
        """

        # Add the user prompt to the conversation history
        conversation_history.append((prompt, "user"))
        messages = self.get_messages_content(conversation_history=conversation_history)

        try:
            # Prepare the function definitions
            functions = [
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
            ]

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                functions=functions,
                function_call="auto",
            )

            choice_message = response.choices[0].message if response else None

            if choice_message and isinstance(
                choice_message.function_call, FunctionCall
            ):
                function_result = self.execute_function(
                    function_call=choice_message.function_call
                )
                self._update_conversation_history_with_function_result(
                    conversation_history, prompt, function_result
                )
                messages = self.get_messages_content(
                    conversation_history=conversation_history
                )
                
                response = self.client.chat.completions.create(
                    model=model, messages=messages
                )
                return (
                    response.choices[0].message.content if response else choice_message.content
                )

            return (
                choice_message.content
                if choice_message
                else "Sorry, I could not process your request."
            )
        except Exception as e:
            logger.error(f"Error on Azure OpenAI endpoint. Exception: {e}")
            return "Sorry, I could not process your request."

    def _update_conversation_history_with_function_result(
        self,
        conversation_history: List[Tuple[str, str]],
        prompt: str,
        function_result: str,
    ) -> None:
        conversation_history.pop()  # Remove previous user prompt
        modified_prompt = f"{prompt}\n\nAdditional Context: {function_result}"
        conversation_history.append((modified_prompt, "user"))


if __name__ == "__main__":
    client = OpenAIClient()
    response = client.get_response(
        "What is langchain", [("You are a helpful assistant.", "system")]
    )
    print(response)
