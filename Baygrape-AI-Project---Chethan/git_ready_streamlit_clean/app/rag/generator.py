import google.generativeai as genai
from app.config import GOOGLE_API_KEY

# Configure Gemini

genai.configure(api_key=GOOGLE_API_KEY)

# Free working model
MODEL_NAME = "gemini-3-flash-preview"

def generate_answer(context: str, question: str, chat_history: str = ""):
prompt = f"""
You are a friendly and intelligent AI assistant.

You may receive document context retrieved from embedded documents.

Follow these rules carefully:

1. If the user's question is related to the embedded documents and the provided context is relevant, use that context in your answer.
2. If the question is general knowledge (e.g., history, science, technology, etc.), answer normally using your own knowledge.
3. If the question is casual conversation (e.g., greetings, small talk), respond naturally and conversationally.
4. If the context is irrelevant to the question, ignore it completely.
5. Do not mention "context" or "knowledge base" in your answer.

Conversation history:
{chat_history}

Document context:
{context}

User question:
{question}

Provide a clear, helpful, and natural response.
"""


    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    return response.text




