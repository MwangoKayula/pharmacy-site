# pharmacy/services/cohere_service.py
import cohere
from django.conf import settings

class CohereService:
    def __init__(self):
        # Initialize the Cohere client with your API key from settings
        self.client = cohere.Client(api_key=settings.COHERE_API_KEY)

    def ask_question(self, question):
        """Sends a question to the Cohere Chat API and returns the answer."""
        if not question or not question.strip():
            return "Please ask a valid question."

        try:
            # Using the chat endpoint
            response = self.client.chat(
                model="command-r-plus",  # Using the latest robust model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful and knowledgeable pharmacy assistant. "
                        "Your answers should be factual, clear, and provide accurate health and medication information. "
                        "Always recommend consulting a doctor or pharmacist for serious medical concerns."
                    },
                    {"role": "user", "content": question}
                ],
                temperature=0.3, # Lower temperature for more factual responses
            )
            # Extract the text of the reply from the assistant
            return response.message.content[0].text
        except Exception as e:
            # Log the error for debugging
            print(f"Cohere API error: {e}")
            return "I'm sorry, the AI service is currently unavailable. Please try again later."
