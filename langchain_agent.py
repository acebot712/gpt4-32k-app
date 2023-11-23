from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class LangChainAgent:
    def init(self):
        tool_names = ["ddg-search", "google-search"]
        self.tools = load_tools(tool_names)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
            deployment_name=os.environ.get("DEPLOYMENT_NAME"),
            openai_api_version=os.environ.get("OPENAI_API_VERSION"),
            openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            model_name=os.environ.get("MODEL_NAME"),
        )
        self.agent_chain = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            max_iterations=5,
        )

    def get_response(self, prompt):
        response = self.agent_chain.invoke(
            {"input": prompt}
        )
        return response["output"]

def main():
    # Initialize the agent
    agent = LangChainAgent()
    agent.init()

    # Provide your input 
    user_prompt = 'Tell me about Yourself'

    # Get the response
    response = agent.get_response(user_prompt)

    # Print the response
    print(response)


if __name__ == "__main__":
    main()
