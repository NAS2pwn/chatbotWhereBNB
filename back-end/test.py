from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

format_instructions = """Tu es un guide touristique qui donne des conseils avisés à un utilisateur qui veut partir en voyage pour lui trouver un logement adéquat sur une plateforme de voyage. Ton rôle est de récolter les envies de l'utilisateur et de l'orienter dans son choix en le conseillant. Soit concis dans tes conseils.

Tu as besoin de récolter : le lieu de location (région, ville ou quartier) final, le budget et le nombre de personnes avec qui il voyage

Ne soit pas trop direct dans tes demandes, il faut d'abord orienter l'utilisateur en lui demandant ce qu'il aimerait plutôt que d'exiger une précision totale dès le début.

Ce n'est pas fini tant qu'il n'a pas validé un logement ou exprimé l'intention de mettre fin à la conversation. Une fois que c'est fini répond lui 'Merci d'avoir choisi WhereBNB !'"""

template = """
{format_instructions}

Current conversation:
{history}
Human: {input}
AI Assistant:"""

prompt = PromptTemplate(
    template=template,
    input_variables=["history", "input"],
    partial_variables={"format_instructions": format_instructions},
)

memory = ConversationBufferMemory(ai_prefix="AI Assistant")

llm = ChatOpenAI(model="gpt-3.5-turbo", streaming=True)

conversation = ConversationChain(
    llm=llm,
    prompt=prompt,
    verbose=False,
    memory=memory
)

print(f"Prompt input schema : {prompt.input_schema.schema()}")
print(f"ConversationChain input schema : {conversation.input_schema.schema()}")

print(f"Prompt output schema : {prompt.output_schema.schema()}")
print(f"ConversationChain output schema : {conversation.output_schema.schema()}")
