import os
from google import genai
from django.conf import settings

class GeminiAssistant:
    def __init__(self):
        # Use the new client
        self.client = genai.Client(api_key=settings.GOOGLE_GEMINI_API_KEY)
        # Available models: gemini-2.0-flash, gemini-1.5-flash, gemini-2.0-flash-lite
        self.model_name = "gemini-2.0-flash"

    def ask_question(self, question):
        if not question or not question.strip():
            return "Please ask a clear question about medications or health."

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=question
            )
            return response.text
        except Exception as e:
            print(f"Gemini error: {e}")
            return "I'm sorry, I couldn't process your request. Please try again later."