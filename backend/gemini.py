import requests

GEMINI_API_URL = "https://api.google.com/gemini"
GEMINI_API_KEY = "your_gemini_api_key"


def generate_narrative(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("choices")[0].get("text")
    else:
        raise Exception("Failed to generate narrative")
