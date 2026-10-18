
from src.models.model_client import OllamaModelClient


def recommend_jobs(
    education,
    skills,
    experience,
    interests,
    location="Finland",
    language="English",
    total_experience=0
):
    """Recommend career roles based on a job seeker's profile."""

    if not education.strip() and not skills.strip():
        return "Please enter your education or skills."

    prompt = f"""
You are CareerPilot, an AI career advisor.

Job seeker profile:
Education: {education}
Skills: {skills}
Work experience: {experience}
Total Work Experience: {total_experience} years
Career interests: {interests}
Preferred job location: {location}
Response language: {language}

Recommend 5 suitable job roles based on this profile.

For each role, provide:
1. Job title
2. Why this role matches the user's profile
3. Relevant existing skills
4. Skills the user should develop

Instructions:
- Write the entire response in {language}.
- Consider the job market and career requirements in {location}.
- Do not invent qualifications or work experience.
- Do not claim these are verified job vacancies.
- Do not invent salary information.
- If information is missing, mention the uncertainty.
"""

    client = OllamaModelClient(model_name="llama3.2:3b")

    try:
        return client.generate(prompt)
    except Exception as error:
        return f"Unable to generate recommendations: {error}"

