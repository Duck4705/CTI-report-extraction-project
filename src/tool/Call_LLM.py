from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


load_dotenv()

# Function to call LLM with optional structured output
def call_LLM(output_schema=None, temperature=0.1):
    OLLAMA = os.getenv("OLLAMA", "false").lower()
    MODEL = os.getenv("MODEL", "Qwen2.5-coder:7b")
    BASE_URL = os.getenv("BASE_URL", "")
    API_KEY = os.getenv("API_KEY", "")
    if OLLAMA == "true":
        base_llm = ChatOllama(model=MODEL, temperature=temperature)
    else:
        if BASE_URL:
            base_llm = ChatOpenAI(model=MODEL, temperature=temperature, base_url=BASE_URL, api_key=API_KEY)
        else:
            base_llm = ChatOpenAI(model=MODEL, temperature=temperature, api_key=API_KEY)
    
    if output_schema is not None:
        structured_llm = base_llm.with_structured_output(output_schema)
        return structured_llm
    
    return base_llm    