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
    You are an expert technical recruiter, hiring manager, and ATS resume evaluator.

    Analyze the candidate's resume against the provided job requirements.

    Resume:
    {resume_text}

    Job Requirements:
    {context}

    Evaluation Guidelines:

    1. First identify all important required skills, technologies, experience requirements, leadership requirements, and communication requirements from the job description.
    2. Compare each requirement against the resume and determine whether it is:
        - Present
        - Partially Present
        - Missing
    3. Calculate a realistic match score from 0-100 using the following weighting:
        - Required Technical Skills: 60%
        - Relevant Work Experience: 20%
        - Leadership & Communication: 20%
    4. Scoring Rules:
        - Missing required technical skills must reduce the score significantly.
        - Good-to-have skills should have only minor impact.
        - Leadership and years of experience should not fully compensate for missing core technical requirements.
        - A candidate missing several required technologies should not receive an excessively high score.
        - The score should reflect how likely the candidate would be shortlisted for this specific role.
    5. Before assigning the final score, internally compare the required skills with the resume and consider both strengths and gaps.

    Return the response in exactly the following format:

    Match Score: /100

    Summary:
    <2-4 sentence explanation of the overall fit>

    Missing Skills:

    - Skill 1: explanation
    - Skill 2: explanation
    - Skill 3: explanation

    Improvement Suggestions:

    - Suggestion 1
    - Suggestion 2
    - Suggestion 3

    Recommended Additional Skills:

    - Skill 1
    - Skill 2
    - Skill 3

    Important:

    - Do not write "No missing skills" unless every required skill is present.
    - Do not invent skills that are not mentioned in the job description.
    - Only list genuinely missing or partially missing skills.
    - Ensure the match score is consistent with the identified missing skills.
    - If multiple required technologies are missing, reduce the score accordingly.
    """

    # prompt = f"""
    # You are an expert technical recruiter, hiring manager, and ATS resume evaluator.

    # Resume Text: 
    # {resume_text}

    # Job description:
    # {context}

    # Tasks: 
    # 1. Give a match score (0-100) 
    # 2. Identify missing skills 
    # 3. Suggest improvements 
    # 4. Recommend additional skills
    # """



    response = llm.invoke(prompt)
    print(response)
    return response.content
