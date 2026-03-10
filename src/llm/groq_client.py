from langchain_groq import ChatGroq
from src.config.setting import setting

def groq_llm():
    return ChatGroq(
        api_key=setting.GROQ_API_KEY,
        model_name=setting.MODEL_NAME,
        temperature=setting.TEMPERATURE
    )