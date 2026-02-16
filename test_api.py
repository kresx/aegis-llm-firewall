import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file.")
else:
    print(f"found API Key: {api_key[:8]}***")

client = OpenAI(api_key=api_key)

try:
    print("Testing connection to OpenAI")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'Aegis System Online'"}],
        max_tokens=10
    )
    print(f"Response: {response.choices[0].message.content}")
    print("API connection successful!")
except Exception as e:
    print(f"API Test Failed: {e}")