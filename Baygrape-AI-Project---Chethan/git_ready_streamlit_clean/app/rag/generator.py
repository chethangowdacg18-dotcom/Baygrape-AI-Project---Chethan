import google.generativeai as genai
from app.config import GOOGLE_API_KEY

# Configure Gemini

genai.configure(api_key=GOOGLE_API_KEY)

# Free working model
MODEL_NAME = "gemini-3-flash-preview"

def generate_answer(context: str, question: str, chat_history: str = ""):
    prompt = f"""
You are an intelligent AI assistant.

You may receive document context from a knowledge base.

If the context is relevant to the user's question, use it to answer.

If the context is empty or not relevant, answer normally using your general knowledge.

Conversation history:
{chat_history}

Context from documents:
{context}

User question:
{question}

Provide a clear and helpful answer.
"""

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    return response.text



