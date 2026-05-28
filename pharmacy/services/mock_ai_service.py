# pharmacy/services/mock_ai_service.py

class MockAIService:
    """
    A mock AI assistant that responds to pharmacy-related questions
    using simple keyword matching. This is for demonstration purposes.
    """

    def ask_question(self, question):
        q = question.lower().strip()
        if not q:
            return "Please ask a question about medications or health."

        # Medication dosage advice
        if "paracetamol" in q or "acetaminophen" in q:
            return ("The typical adult dose of paracetamol is 500mg every 4-6 hours, "
                    "not exceeding 3000mg per day. Always follow the label instructions.")
        if "ibuprofen" in q:
            return ("Ibuprofen for adults: 200-400mg every 6-8 hours as needed, "
                    "max 1200mg per day. Take with food to avoid stomach upset.")
        if "aspirin" in q:
            return ("Aspirin: 300-600mg every 4-6 hours for pain/fever. "
                    "Do not give to children under 16 unless prescribed.")
        if "amoxicillin" in q:
            return ("Amoxicillin is an antibiotic. Dosage depends on the infection. "
                    "Always complete the full course as prescribed by your doctor.")

        # Common health questions
        if "headache" in q:
            return ("For headaches, try over-the-counter paracetamol or ibuprofen. "
                    "Drink water, rest, and avoid bright screens. If severe or persistent, "
                    "consult a pharmacist or doctor.")
        if "cold" in q or "flu" in q:
            return ("For cold/flu symptoms: rest, stay hydrated, and use paracetamol for fever. "
                    "Over-the-counter decongestants may help. Consult a pharmacist for children.")
        if "allergy" in q:
            return ("Antihistamines like loratadine or cetirizine can help with allergies. "
                    "For severe reactions, seek medical attention immediately.")
        if "vitamin" in q or "supplement" in q:
            return ("Vitamins and supplements are best obtained from a balanced diet. "
                    "Consult a healthcare professional before starting any new supplement.")

        # General help
        if "hello" in q or "hi" in q:
            return "Hello! I'm your pharmacy assistant. How can I help you today?"
        if "thank" in q:
            return "You're welcome! Stay healthy."

        # Default fallback
        return ("I'm here to help with medication questions. Please ask about specific drugs, "
                "dosages, side effects, or general health advice. For medical emergencies, "
                "call your doctor or emergency services immediately.")