import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv('LLM_API_KEY')
        self.model = "openrouter/meta-llama/llama-3.1-8b-instruct:free"

    def ask_question(self, question):
        try:
            response = completion(
                model=self.model,
                messages=[{"content": question, "role": "user"}],
                api_key=self.api_key,
                api_base="https://openrouter.ai/api/v1"
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error contacting LLM: {e}")
            return "Sorry, the AI service is temporarily unavailable."