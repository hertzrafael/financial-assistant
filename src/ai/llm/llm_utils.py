from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from dotenv import load_dotenv
from os import getenv


load_dotenv()

def _load_llm() -> BaseChatModel:
    llm = init_chat_model(
        'openai:gpt-4.1-mini',
        temperature=0.2,
        api_key=getenv('OPENAI_API_KEY'),
    )

    return llm


llm = _load_llm()
