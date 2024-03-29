import os
from typing import Dict, List, Any

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain.globals import set_debug

from callbacks.mycallback import MyCallbackHandler


def has_action(last_message: str) -> bool:
    if os.getenv("MODE") == "development":
        callbacks = [MyCallbackHandler("mhas_action")]
    else:
        callbacks = None
        
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        callbacks=callbacks,
    )

    instructions = """given the following message from a touristic advisor
    {last_message}

    I want you to evaluate if he is currently using WhereBNB to search a flat as he say it explicitly

    If a search action is occurring now, return true
    If he is just chatting, return false
    If he is asking for information in order to perform a search but he is not performing a search, return false

    Don't return anything but true or false, all lowcap
    """

    prompt = PromptTemplate(input_variables=['last_message'], template=instructions)

    chain = (
            prompt
            | llm
            | JsonOutputParser()
    )

    return chain.invoke({"last_message": last_message})


def fetch_action(history: List[BaseMessage]) -> Dict[str, Any]:
    if os.getenv("MODE") == "development":
        callbacks = [MyCallbackHandler("fetch_actions")]
    else:
        callbacks = None
        
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        callbacks=callbacks,
    )

    instructions = """we are in 2024, given the following conversation

    {history}

    I want to you to understand what the AI is trying to looking for on WhereBNB and convert it to a JSON.

    First, you have to understand the situation. AI is looking for an accommodation in a certain city, from a date to another date, for n guests, with a budget of x€ a day.

    Then, you have to forge the request as follow

    Situation : AI is looking for an accommodation in Soho from the 5th May to the 14th May, for 3 guests, with a budget of 100€ a day.
    Output : {{"action" : "search", "params" : {{"location" : "Soho, London, England", "check_in": "2024-05-10", "check_out": "2024-05-14", "guests_number" : 3, "budget_per_day" : 100}}}}
    """

    prompt = PromptTemplate(input_variables=['history'], template=instructions)

    chain = (
        {"history": lambda x: ChatPromptTemplate.from_messages(x).format()}
        | prompt
        | llm
        | JsonOutputParser()
    )

    return chain.invoke(history)
