from fastapi import FastAPI
from pydantic import BaseModel
from vector_db import query_chunks
import google.generativeai as genai
import os

# Load your Gemini API key (replace 'YOUR_API_KEY')
GEMINI_API_KEY = "AIzaSyDX3xSrhde3T7GIOZJVCyDDHIvNnn4uxwo"
genai.configure(api_key=GEMINI_API_KEY)

# Create a Gemini model instance
model = genai.GenerativeModel('gemini-2.0-flash')

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query_meeting(request: QueryRequest):
    # Search chunks
    contexts = query_chunks(request.question)

    # Simple context → answer generation
    answer = generate_answer(request.question, contexts)

    return {
        "answer": answer,
        "matched_contexts": contexts
    }

def generate_answer(question, contexts):
    prompt = f"""
You are an assistant that helps answer questions based on meeting notes.

Meeting Notes:
{chr(10).join(contexts)}

Question: {question}

Answer:
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error using Gemini API: {e}")
        return "❌ Error generating answer."
