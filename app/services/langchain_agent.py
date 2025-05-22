import os
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from app.services.langchain_tools import describe_table

llm = ChatOpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    default_headers={"X-API-KEY": os.getenv("AZURE_OPENAI_API_KEY")},
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    temperature=0.7,
    max_tokens=500,
)

agent = initialize_agent(
    tools=[describe_table],
    llm=llm,
    agent="chat-conversational-react-description",
    verbose=True
)
