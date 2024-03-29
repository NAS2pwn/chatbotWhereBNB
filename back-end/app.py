import os
import threading
import time
from typing import List, Any
import json

from fastapi import FastAPI, WebSocket
from dotenv import load_dotenv
from apify_client import ApifyClient

from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAI
from callbacks.mycallback import MyCallbackHandler

from agents.action_router import fetch_action, has_action

load_dotenv()
app = FastAPI()


def print_dots(stop_event: threading.Event):
    """Affiche un point toutes les 2 secondes jusqu'à ce que stop_event soit défini."""
    while not stop_event.is_set():
        print('...', end='', flush=True)
        time.sleep(0.5)


def airbnb_search(
    location_query: str,
    check_in: str,
    check_out: str,
    budget_per_day: int,
    guests_number: int,
) -> List[Any] :
    apify = ApifyClient(os.getenv("APIFY_API_KEY"))
    run_input = {
        "locationQuery": location_query,
        "maxListings": 10,
        "simple": True,
        "startUrls": [],
        "includeReviews": False,
        "maxReviews": 10,
        "calendarMonths": 0,
        "addMoreHostInfo": False,
        "currency": "EUR",
        "checkIn": check_in,
        "checkOut": check_out,
        "proxyConfiguration": { "useApifyProxy": True },
        "maxConcurrency": 50,
        "limitPoints": 100,
        "timeoutMs": 60000,
        "debugLog": False,
    }

    stop_event = threading.Event()
    dot_thread = threading.Thread(target=print_dots, args=(stop_event,))
    dot_thread.start()

    try:
        run = apify.actor(os.getenv("APIFY_AIRBNB_ACTOR_ID")).call(run_input=run_input)
    finally:
        stop_event.set()
        dot_thread.join()

    output = []

    all_price_guests = []

    for item in apify.dataset(run["defaultDatasetId"]).iterate_items():
        if item['pricing']['rate']['amount'] <= budget_per_day and item['numberOfGuests'] >= guests_number :
            output.append(item)

        all_price_guests.append({'prix': item['pricing']['rate']['amount'], 'nb_guests': item['numberOfGuests']})

    return output

format_instructions = """Tu es un conseiller touristique qui s'adresse à un client qui veut partir en voyage.

Ton rôle est de comprendre les envies de l'utilisateur en terme de voyage et de lui faire des recommandations en fonction.

L'échange se déroule en trois étapes :
1. Tu discutes avec l'utilisateur pour comprendre ses envies, d'abord tu lui demandes le type de voyage qu'il veut, puis tu le recommandes et t'essayes toujours de lui proposer des alternatives.
Durant cette phase, tu conseilleras l'utilisateur et ne lui posera pas de question sur la phase suivante de récolte d'infos
Cette phase se termine quand l'utilisateur aura définitivement choisi un lieu.
2. Une fois qu'il a choisi le lieu, il faut que tu récoltes : les dates, le nombre de personnes qui voyagent, le budget par jour.
Cette phase se termine uniquement quand tu as récolté les dates ET le nombre de personnes qui voyagen ET le budget par jour.
3. Tu lances la recherche en écrivant "Parfait, je recherche un logement adapté à vos critères <liste les critères> sur la plateforme WhereBNB.
Si l'utilisateur veut lancer une recherche sans être passé par l'étape 2 de récolte de données, tu dis "Je ne peux pas lancer de recherche sans avoir les dates du voyage, le budget journalier et le nombre de voyageurs"

Aère tes messages en sautant fréquemment de ligne, et ait un niveau de précision contrôlé, ne parle pas trop, va à l'essentiel
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", format_instructions),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

memory = ConversationSummaryBufferMemory(llm=OpenAI(temperature=0), max_token_limit=1000, return_messages=True)

if os.getenv("MODE") == "development":
    callbacks = [MyCallbackHandler("main conversation")]
else:
    callbacks = None

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    streaming=True,
    callbacks=callbacks,
)

conversation = (
    prompt
    | llm
    | StrOutputParser()
)

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    history = memory.load_memory_variables({})['history']#[]

    while True:
        user_message_text = await websocket.receive_text()

        response = ""

        async for chunk in conversation.astream(input={"input": user_message_text, "history": history}):
            await websocket.send_text(chunk)
            response += chunk

        memory.save_context({"input": user_message_text}, {"output": response})
        memory_variables = memory.load_memory_variables({})
        history = memory_variables['history']

        if has_action(response):
            action = fetch_action(history)
            params = action['params']

            search_results = airbnb_search(
                location_query=params['location'],
                check_in=params['check_in'],
                check_out=params['check_out'],
                budget_per_day=params['budget_per_day'],
                guests_number=params['guests_number'],
            )

            await websocket.send_text('\n')

            for result in search_results[:5]:
                await websocket.send_text(f"\n{result['name']}\n{result['url']}\n\n")