from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        groq_api_key = groq_api_key
    )

def generate_response(llm, resume_text, retrieved_docs):
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    prompt = f"""
    You are an AI resumse analyzer.

    Resume:
    {resume_text}

    Job Requirements:
    {context}

    Instructions:

Evaluate the candidate against the job requirements using the following criteria:

1. Technical Skills Match (60%)
   - Compare required technical skills against the resume.
   - Missing required skills should significantly reduce the score.
   - Good-to-have skills should have minimal impact.

2. Experience Match (20%)
   - Compare years of experience and relevant work history.

3. Leadership & Communication (20%)
   - Evaluate project leadership, stakeholder management, mentoring, and client interaction.

Scoring Rules:
- If more than 40% of required technical skills are missing, the score should not exceed 75.
- If more than 60% of required technical skills are missing, the score should not exceed 65.
- Do not reward experience or leadership enough to compensate for major technical gaps.

    """

    response = llm.invoke(prompt)
    return response.content
