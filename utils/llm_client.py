import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_groq import ChatGroq

load_dotenv()

def get_llm() -> BaseChatModel:
    use_groq = os.getenv("USE_GROQ", "False").lower() == "true"
    model_name = os.getenv("LLM_MODEL", "mixtral-8x7b-32768")

    if use_groq:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not set in .env")
        print("Using Groq LLM")

        # For langchain-groq version 0.1.3, use these exact parameters
        return ChatGroq(
            api_key=groq_api_key,
            model=model_name,
            temperature=0.2,
            max_retries=2
        )
    else:
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not set in .env")
        print("Using OpenAI LLM")
        return ChatOpenAI(
            api_key=openai_key,
            model=model_name,
            temperature=0.2
        )