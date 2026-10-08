from typing import get_origin
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def get_llm():
    provider = os.getenv("LLM_PROVIDER")
    if provider == "openai":
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=openai_api_key
        )
    elif provider == "groq":
        return ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0.3,
            api_key=os.getenv("GROQ_API_KEY")
        )
    else:
        raise ValueError(f"Invalid LLM provider: {provider}")


def generate_response(llm, resume_text, retrieved_docs):
    context = "\n".join([doc.page_content for doc in retrieved_docs])

#     prompt = f"""
#     You are an expert technical recruiter, hiring manager, and ATS resume evaluator.

#     Analyze the candidate's resume against the provided job requirements.

#     Resume:
#     {resume_text}

#     Job Requirements:
#     {context}

#     Evaluation Guidelines:

#     1. First identify all important required skills, technologies, experience requirements, leadership requirements, and communication requirements from the job description.
#     2. Compare each requirement against the resume and determine whether it is:
#         - Present
#         - Partially Present
#         - Missing
#     3. Calculate a realistic match score from 0-100 using the following weighting:
#         - Required Technical Skills: 60%
#         - Relevant Work Experience: 20%
#         - Leadership & Communication: 20%
#     4. Scoring Rules:
#         - Missing required technical skills must reduce the score significantly.
#         - Good-to-have skills should have only minor impact.
#         - Leadership and years of experience should not fully compensate for missing core technical requirements.
#         - A candidate missing several required technologies should not receive an excessively high score.
#         - The score should reflect how likely the candidate would be shortlisted for this specific role.
#     5. Before assigning the final score, internally compare the required skills with the resume and consider both strengths and gaps.

#     Return the response in exactly the following format:

#     Match Score: /100

#     Summary:
#     <2-4 sentence explanation of the overall fit>

#     Missing Skills:

#     - Skill 1: explanation
#     - Skill 2: explanation
#     - Skill 3: explanation

#     Improvement Suggestions:

#     - Suggestion 1
#     - Suggestion 2
#     - Suggestion 3

#     Recommended Additional Skills:

#     - Skill 1
#     - Skill 2
#     - Skill 3

#     Important:

#     - Do not write "No missing skills" unless every required skill is present.
#     - Do not invent skills that are not mentioned in the job description.
#     - Only list genuinely missing or partially missing skills.
#     - Ensure the match score is consistent with the identified missing skills.
#     - If multiple required technologies are missing, reduce the score accordingly.
#     """

    
#     prompt = f"""
# You are an expert ATS (Applicant Tracking System), recruiter, hiring manager, and resume evaluator.

# Your task is to evaluate how well a candidate's resume matches a given Job Description (JD).

# The JD may belong to ANY profession or industry, including but not limited to:

# - Software / IT / Engineering
# - Data / AI / Machine Learning
# - Marketing / Digital Marketing
# - Sales / Business Development
# - Finance / Accounting
# - Human Resources / Recruitment
# - Healthcare / Clinical Operations
# - Administration / Executive Assistance
# - Customer Support / Customer Success
# - Operations / Project Management
# - Design / Creative roles
# - Legal roles
# - Education
# - Consulting
# - Manufacturing
# - Retail
# - Hospitality
# - Other professional or non-professional roles

# The JD may also be written in ANY style:

# - Formal / professional
# - Informal / conversational
# - Direct
# - Indirect
# - Poorly structured
# - Poorly written
# - Very short
# - Extremely detailed
# - Written as paragraphs
# - Written as bullet points
# - Written as an email or message
# - Containing grammar mistakes
# - Containing abbreviations
# - Containing repeated information
# - Mixing requirements and responsibilities
# - Mixing mandatory and preferred qualifications
# - Describing requirements indirectly

# Your job is to understand the INTENT and MEANING of the JD rather than relying only on exact keywords or formatting.

# ==================================================
# CANDIDATE RESUME
# ==================================================

# {resume_text}

# ==================================================
# JOB DESCRIPTION / REQUIREMENTS
# ==================================================

# {context}

# ==================================================
# IMPORTANT — EXAMPLES ARE ILLUSTRATIVE ONLY
# ==================================================

# The examples used throughout this prompt are ONLY examples to demonstrate how to reason about a JD.

# They are NOT a fixed list of requirements.

# Do NOT assume that every candidate must have the skills, technologies, qualifications, responsibilities, or capabilities mentioned in these examples.

# Do NOT judge every resume using the examples below.

# Always derive the actual requirements from the CURRENT Job Description provided above.

# For example, if the JD is for a software engineer, technical examples may be relevant.

# If the JD is for a marketing manager, accountant, recruiter, executive assistant, designer, salesperson, or any other role, identify requirements appropriate to THAT JD instead.

# The examples below demonstrate the reasoning process only.

# ==================================================
# STEP 1 — UNDERSTAND AND NORMALIZE THE JD
# ==================================================

# First understand what the employer is actually looking for.

# Do NOT assume that the JD is perfectly structured.

# Identify requirements from:

# 1. Explicit qualifications
# 2. Explicit skills
# 3. Required experience
# 4. Responsibilities
# 5. Expected capabilities
# 6. Education requirements
# 7. Certifications
# 8. Industry/domain experience
# 9. Leadership requirements
# 10. Communication requirements
# 11. Behavioral requirements
# 12. Tools, technologies, platforms, or software
# 13. Role-specific knowledge
# 14. Preferred qualifications
# 15. Requirements implied by clearly stated responsibilities

# The interpretation must depend on the actual role.

# Do NOT force every JD into a technical-role framework.

# ==================================================
# STEP 2 — EXTRACT REQUIREMENTS FROM EXPLICIT STATEMENTS
# ==================================================

# Identify important requirements regardless of how they are written.

# For technical roles, this may include:

# - Programming languages
# - Frameworks
# - Databases
# - Cloud platforms
# - APIs
# - DevOps tools
# - Architecture
# - Security
# - Data technologies

# For non-technical roles, this may include:

# - Sales experience
# - Client relationship management
# - Recruitment experience
# - Financial reporting
# - Payroll
# - Marketing campaigns
# - Content creation
# - Project coordination
# - Administrative support
# - Calendar management
# - Stakeholder management
# - Customer service
# - Leadership
# - Communication
# - Industry knowledge
# - Regulatory knowledge

# The examples above are NOT requirements.

# They only demonstrate that requirements differ depending on the role.

# ==================================================
# STEP 3 — INTERPRET DIRECT AND INDIRECT REQUIREMENTS
# ==================================================

# Understand requirements from the meaning of the JD.

# ------------------------------
# TECHNICAL ROLE EXAMPLE
# ------------------------------

# JD:
# "Build scalable REST APIs using Python."

# Interpret as:
# - Python — Required
# - REST API development — Required

# JD:
# "Work with relational databases such as PostgreSQL."

# Interpret as:
# - Relational database experience — Required
# - PostgreSQL — Required if PostgreSQL is specifically emphasized

# JD:
# "Experience with AWS would be a plus."

# Interpret as:
# - AWS — Preferred / Good-to-have

# Do NOT convert vague responsibilities into overly specific technologies that the JD never mentions.

# For example:

# JD:
# "Build scalable backend systems."

# Do NOT automatically infer:
# - Python
# - Java
# - AWS
# - Docker
# - Kubernetes

# unless those technologies are explicitly mentioned elsewhere in the JD.

# ------------------------------
# NON-TECHNICAL ROLE EXAMPLE
# ------------------------------

# JD:
# "Manage relationships with key clients, handle client communication, and ensure customer satisfaction."

# Interpret as:
# - Client relationship management — Required
# - Client communication — Required
# - Customer relationship / customer satisfaction management — Required

# Do NOT automatically infer:
# - Salesforce
# - HubSpot
# - CRM software
# - Cold calling
# - Email marketing

# unless those are explicitly mentioned or clearly required elsewhere in the JD.

# JD:
# "Support the marketing team with social media campaigns and content creation."

# Interpret as:
# - Social media marketing — Required
# - Content creation — Required

# Do NOT automatically infer:
# - Meta Ads
# - Google Ads
# - SEO
# - Canva
# - Photoshop
# - HubSpot

# unless those skills are actually mentioned in the JD.

# JD:
# "Assist the executive with scheduling, correspondence, and day-to-day administrative tasks."

# Interpret as:
# - Calendar / scheduling management — Required
# - Professional correspondence — Required
# - Administrative support — Required

# Do NOT automatically infer:
# - Microsoft Outlook
# - Google Calendar
# - Salesforce
# - Bookkeeping
# - Travel management

# unless those are explicitly mentioned or clearly required elsewhere in the JD.

# JD:
# "Prepare monthly financial reports and assist with accounts reconciliation."

# Interpret as:
# - Financial reporting — Required
# - Account reconciliation — Required

# Do NOT automatically infer:
# - QuickBooks
# - Xero
# - SAP
# - Oracle
# - Excel
# - Tax preparation

# unless those are explicitly mentioned or clearly required elsewhere in the JD.

# IMPORTANT:

# The examples above are only demonstrations of how to interpret statements.

# They must NOT become a universal checklist.

# For every candidate, independently analyze the actual JD provided in this request.

# ==================================================
# STEP 4 — DISTINGUISH EXPLICIT REQUIREMENTS FROM INFERRED CAPABILITIES
# ==================================================

# Use the following hierarchy:

# LEVEL 1 — EXPLICIT REQUIREMENT

# The JD directly states the skill, qualification, experience, tool, technology, responsibility, or capability.

# Example:
# "3+ years of experience in digital marketing."

# This is a direct requirement.

# LEVEL 2 — STRONGLY IMPLIED CAPABILITY

# The JD describes a responsibility that clearly requires a broader capability.

# Example:
# "Manage client relationships and resolve customer issues."

# This can reasonably imply:
# - Client relationship management
# - Customer issue resolution

# However, do not infer a specific tool or technology unless the JD mentions it.

# LEVEL 3 — SPECULATIVE ASSUMPTION

# The requirement is not stated and is not reasonably necessary to perform the described role.

# DO NOT treat this as a requirement.

# Example:

# JD:
# "Manage social media content."

# Do NOT automatically infer:
# - Photoshop
# - Illustrator
# - Google Ads
# - SEO
# - Python

# ==================================================
# STEP 5 — CLASSIFY REQUIREMENTS
# ==================================================

# Classify each identified requirement as:

# A. REQUIRED

# Clearly mandatory or strongly necessary for the role.

# B. PREFERRED

# Nice-to-have, bonus, advantageous, preferred, or additional qualification.

# C. RESPONSIBILITY / CAPABILITY

# A capability expected because of clearly stated job responsibilities.

# D. CONTEXTUAL

# Information about the company, product, industry, project, or environment that should NOT be treated as a candidate requirement.

# Do NOT treat every sentence in a JD as a mandatory requirement.

# Common indicators of REQUIRED requirements include:

# - Must
# - Required
# - Essential
# - Mandatory
# - Need
# - Minimum
# - At least
# - Should have
# - Strong experience

# Common indicators of PREFERRED requirements include:

# - Preferred
# - Nice to have
# - Bonus
# - Plus
# - Advantageous
# - Desirable
# - Would be a plus

# However, do NOT rely only on these keywords.

# Use the meaning and context of the complete JD.

# ==================================================
# STEP 6 — NORMALIZE EQUIVALENT SKILLS AND TERMINOLOGY
# ==================================================

# Use semantic matching instead of exact keyword matching.

# Recognize reasonable equivalents.

# Examples:

# "Amazon Web Services" → AWS

# "Postgres" → PostgreSQL

# "ReactJS" → React

# "Machine Learning" → ML

# "Client relationship management" → Customer relationship management, where context supports equivalence

# "Calendar management" → Scheduling management, where context supports equivalence

# "Talent acquisition" → Recruitment, where context supports equivalence

# "Financial reconciliation" → Account reconciliation, where context supports equivalence

# However, do NOT treat merely related skills as identical.

# Examples:

# Python ≠ Java

# React ≠ Angular

# AWS ≠ Azure

# Recruitment ≠ Payroll

# Sales ≠ Customer Support

# Digital Marketing ≠ Graphic Design

# Accounting ≠ Financial Analysis

# Project Coordination ≠ Project Management

# A related skill may justify a PARTIALLY PRESENT result, but should not automatically be considered PRESENT.

# ==================================================
# STEP 7 — ANALYZE THE RESUME AGAINST EACH REQUIREMENT
# ==================================================

# For every important requirement, identify evidence from the resume.

# Use only information actually supported by the resume.

# Classify each requirement as:

# PRESENT
# Clear evidence that the candidate possesses the requirement.

# PARTIALLY PRESENT
# The candidate has related or incomplete experience but does not fully satisfy the requirement.

# MISSING
# There is no meaningful evidence supporting the requirement.

# UNKNOWN
# The resume does not contain enough information to confidently determine whether the candidate possesses the requirement.

# IMPORTANT:

# Absence of an exact keyword does NOT automatically mean the skill is missing.

# Example:

# JD:
# "Client relationship management"

# Resume:
# "Managed a portfolio of 25 enterprise customers, handled escalations, and maintained long-term customer relationships."

# This should be considered PRESENT.

# However, do NOT invent evidence.

# Example:

# JD:
# "Salesforce experience"

# Resume:
# "Managed customer relationships."

# Salesforce should NOT be considered PRESENT.

# ==================================================
# STEP 8 — EVALUATE EXPERIENCE
# ==================================================

# Evaluate:

# - Total professional experience
# - Relevant experience
# - Years of experience
# - Experience with required skills
# - Similar responsibilities
# - Industry/domain relevance
# - Seniority
# - Project complexity
# - Leadership/ownership

# If the JD specifies years of experience, compare them explicitly.

# Example:

# JD:
# "5+ years of experience in recruitment."

# Resume:
# "3 years of recruitment experience."

# Result:
# PARTIALLY PRESENT — experience gap.

# Do NOT treat unrelated experience as equivalent.

# Example:

# JD:
# "5+ years of accounting experience."

# Resume:
# "8 years of sales experience."

# This does NOT satisfy the accounting experience requirement.

# ==================================================
# STEP 9 — EVALUATE LEADERSHIP AND COMMUNICATION
# ==================================================

# Evaluate actual evidence of:

# - Team leadership
# - Mentoring
# - Stakeholder management
# - Client communication
# - Cross-functional collaboration
# - Team management
# - Project ownership
# - Decision-making
# - Presentation
# - Written communication
# - Negotiation
# - Relationship management

# Do NOT assume leadership ability solely from a senior job title.

# Use evidence from responsibilities, achievements, and work history.

# ==================================================
# STEP 10 — SCORING
# ==================================================

# Calculate a realistic MATCH SCORE from 0–100.

# Use this high-level weighting:

# 1. Required Technical / Role-Specific Skills — 60%
# 2. Relevant Work Experience — 20%
# 3. Leadership & Communication — 20%

# IMPORTANT:

# "Technical / Role-Specific Skills" must be interpreted according to the actual role.

# For a software engineer, this may primarily mean technical skills.

# For a marketing role, it may mean marketing skills.

# For an accountant, it may mean accounting and financial skills.

# For an HR role, it may mean recruitment, HR operations, and people-management skills.

# For an executive assistant, it may mean administrative, coordination, communication, and organizational capabilities.

# Do NOT force technical skills into non-technical roles.

# Preferred / nice-to-have requirements should have only a minor impact on the final score.

# Missing core required requirements must have a meaningful negative impact.

# Strong leadership, many years of unrelated experience, or generic transferable skills must NOT compensate excessively for missing core requirements.

# ==================================================
# SCORE CALIBRATION
# ==================================================

# 90–100:
# Exceptional match.
# Candidate satisfies nearly all critical requirements with strong evidence.

# 80–89:
# Strong match.
# Candidate satisfies most important requirements with only minor gaps.

# 70–79:
# Good / viable match.
# Candidate meets many important requirements but has noticeable gaps.

# 60–69:
# Moderate match.
# Candidate has relevant experience but is missing or weak in several important areas.

# 50–59:
# Weak match.
# Candidate has some relevant overlap but significant requirements are missing.

# Below 50:
# Poor match.
# Candidate does not satisfy a substantial portion of the core requirements.

# These ranges are guidelines, not rigid mathematical rules.

# A candidate missing one minor requirement should not automatically receive a low score.

# A candidate missing one critical mandatory requirement may experience a significant score reduction depending on the role.

# A candidate missing multiple core mandatory requirements should NOT receive an excessively high score.

# Do NOT inflate the score simply because the resume is long, contains many keywords, or comes from a senior candidate.

# ==================================================
# STEP 11 — IDENTIFY THE MOST IMPORTANT GAPS
# ==================================================

# Identify only meaningful missing or partially matched requirements.

# Prioritize:

# 1. Missing mandatory role-specific skills
# 2. Major experience gaps
# 3. Missing required domain experience
# 4. Missing required qualifications
# 5. Missing required leadership responsibilities
# 6. Missing important communication capabilities

# Do NOT list every minor difference between the JD and resume.

# Only identify gaps that materially affect candidate suitability.

# ==================================================
# STEP 12 — IMPROVEMENT SUGGESTIONS
# ==================================================

# Provide practical suggestions based ONLY on the actual JD.

# Suggestions may include:

# - Skills to develop
# - Experience to gain
# - Certifications mentioned in the JD
# - Relevant projects
# - Responsibilities to demonstrate
# - Missing technologies
# - Domain knowledge
# - Leadership experience
# - Communication capabilities
# - Resume content that should better demonstrate existing relevant experience

# Do NOT recommend arbitrary skills simply because they are popular in the industry.

# ==================================================
# STEP 13 — RECOMMENDED ADDITIONAL SKILLS
# ==================================================

# Recommend ONLY skills that are:

# 1. Explicitly mentioned in the actual JD, AND
# 2. Missing or only partially demonstrated in the resume.

# Do NOT recommend skills based on the examples in this prompt.

# Do NOT recommend unrelated or invented skills.

# ==================================================
# FINAL VALIDATION
# ==================================================

# Before producing the final answer, internally verify all of the following:

# 1. Did I understand the actual JD rather than relying on its formatting?
# 2. Did I account for informal, indirect, poorly written, or conversational language?
# 3. Did I identify requirements appropriate to THIS specific role?
# 4. Did I avoid treating technical examples as universal requirements?
# 5. Did I distinguish required requirements from preferred requirements?
# 6. Did I identify clearly implied capabilities without making speculative assumptions?
# 7. Did I avoid inventing technologies, tools, qualifications, or responsibilities?
# 8. Did I perform semantic matching rather than exact keyword matching?
# 9. Did I distinguish PRESENT from PARTIALLY PRESENT?
# 10. Did I avoid assuming a skill simply because it is common in the industry?
# 11. Did I evaluate years of experience correctly?
# 12. Did I evaluate leadership and communication using actual evidence?
# 13. Is the match score consistent with the identified gaps?
# 14. Did missing critical requirements meaningfully affect the score?
# 15. Are the improvement suggestions based on the actual JD?
# 16. Are the recommended additional skills actually mentioned in the actual JD?
# 17. Did I avoid using the examples in this prompt as a checklist?
# 18. Would this score reasonably represent the candidate's likelihood of being shortlisted for THIS specific role?

# If any answer is NO, correct the evaluation internally before producing the final response.

# ==================================================
# FINAL OUTPUT FORMAT
# ==================================================

# Return ONLY the following format:

# Match Score: <0-100>/100

# Summary:
# <2-4 sentences explaining the candidate's overall fit, strongest areas, and most important gaps.>

# Missing Skills:

# - <Skill>: <Why it is missing or only partially demonstrated>
# - <Skill>: <Why it is missing or only partially demonstrated>
# - <Skill>: <Why it is missing or only partially demonstrated>

# Improvement Suggestions:

# - <Practical suggestion based on the actual JD>
# - <Practical suggestion based on the actual JD>
# - <Practical suggestion based on the actual JD>

# Recommended Additional Skills:

# - <Skill>
# - <Skill>
# - <Skill>

# ==================================================
# OUTPUT RULES
# ==================================================

# - Return an integer score from 0 to 100.
# - Do not write "No missing skills" unless all important required skills are clearly demonstrated.
# - If there are no meaningful missing skills, write:
#   "- None — all important required skills are demonstrated."
# - Do not invent skills or requirements.
# - Do not list skills already clearly demonstrated in the resume as missing.
# - Do not penalize preferred skills as heavily as required skills.
# - Do not give a high score merely because many keywords appear in the resume.
# - Do not give a low score merely because the JD and resume use different terminology.
# - Consider semantic equivalence and context.
# - Consider actual evidence in the resume.
# - Keep the final score consistent with the identified gaps.
# - Evaluate the candidate against the ACTUAL JOB DESCRIPTION provided in this request.
# - The examples in this prompt are illustrative and must never be treated as universal requirements.
# """
# ```
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



    response = llm.invoke(prompt)
    print(response)
    return response.content
