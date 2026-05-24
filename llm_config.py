import os
from crewai import LLM
from dotenv import load_dotenv


load_dotenv()

llm = LLM(
    model="openrouter/openai/gpt-oss-120b:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    temperature=0.1,
    max_tokens=800,        # limit output per call
    
)