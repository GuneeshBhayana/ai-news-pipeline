import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Initialize client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Ask the API for the list of models you have access to
print("Fetching available models...")
try:
    for model in client.models.list():
        print(f"Model ID: {model.name}")
except Exception as e:
    print(f"Error fetching models: {e}")