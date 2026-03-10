import os
from dotenv import load_dotenv

load_dotenv()

class Setting():
    GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    MODEL_NAME="llama-3.1-8b-instant"
    
    TEMPERATURE=0.9
    
    MAX_RETRIES=3
    
    
setting=Setting()