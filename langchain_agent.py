from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

tool_names = ["ddg-search", "google-search"]

tools = load_tools(tool_names)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = AzureChatOpenAI(
    azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
    deployment_name=os.environ.get("DEPLOYMENT_NAME"),
    openai_api_version=os.environ.get("OPENAI_API_VERSION"),
    openai_api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    model_name=os.environ.get("MODEL_NAME"),
)

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    max_iterations=5,
)

response = agent_chain(
    {
        "input": "Tell me more about yourself"
    }
)
# print(response)
print(response["output"])
