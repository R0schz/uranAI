from google import genai

GEMINI_API_KEY = "AIzaSyCGfERhw9POcFwcuwtOlmoBfbXIIj4CFlQ"

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_narrative(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return response.text
