from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType

def lookup(name: str) -> str:
    return "TODO"