import os
from google import genai
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.local')

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

client = genai.Client(api_key=GOOGLE_GEMINI_API_KEY)

def generate_narrative(prompt: str) -> str:
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite", contents=prompt
    )
    return response.text
