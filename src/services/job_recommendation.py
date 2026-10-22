from src.models.model_client import OllamaModelClient
from src.services.csv_jobs import select_csv_jobs


def recommend_jobs(
    education,
    skills,
    experience,
    interests,
    location="Finland",
    language="English",
    total_experience=0,
):
    education = (education or "").strip()
    skills = (skills or "").strip()
    experience = (experience or "").strip()
    interests = (interests or "").strip()
    location = (location or "Finland").strip()
    language = language if language in {"English", "Finnish", "Swedish"} else "English"

    if not education and not skills:
        return "Please enter your education or skills."

    client = OllamaModelClient(model_name="llama3.2:3b")
    profile = (
        f"Education: {education}\n"
        f"Skills: {skills}\n"
        f"Work experience: {experience}\n"
        f"Total work experience: {total_experience} years\n"
        f"Career interests: {interests}\n"
        f"Preferred location: {location}\n"
    )

    # This is intentionally based on the original application, NOT the CSV.
    role_prompt = f"""You are CareerPilot, an AI career advisor.

Job seeker profile:
{profile}

Recommend exactly 5 DISTINCT possible career roles, NOT individual job advertisements.
These are general career options that may or may not currently have vacancies.

Start with a short greeting like: "Hello! Based on your profile, I've curated five job roles that align with your interests and skills. Here they are:"
For EACH numbered recommendation, use precisely this readable Markdown layout:
**1. Job title**
Why this role matches your profile: (2 concise sentences specific to the profile)
Relevant existing skills: (only skills actually present in the profile)
Skills to develop: (useful suggestions, not claimed requirements)

Repeat the same format for all five roles, numbered 1 through 5. Put blank lines between roles.
Write the ENTIRE response in {language}, translating labels appropriately.
Consider career requirements in {location}.
Do not invent existing skills, qualifications, work experience, salary, or verified vacancies.
Do not list specific vacancies or link to advertisements. Do not add a conclusion.
"""

    output = []
    try:
        output.append(client.generate(role_prompt).strip())
    except Exception as error:
        output.append(f"Unable to generate the five AI career suggestions: {error}")

    output.append("\n---\n")
    section_titles = {
        "English": "### 3 relevant job advertisements",
        "Finnish": "### 3 sopivaa työpaikkailmoitusta",
        "Swedish": "### 3 relevanta jobbannonser",
    }
    output.append(section_titles[language])
    try:
        jobs = select_csv_jobs(
            education, skills, experience, interests, location, total_experience, limit=3
        )
    except (OSError, UnicodeError, ValueError) as error:
        jobs = []
        output.append(f"Could not read the CSV file: {error}")

    if not jobs:
        output.append("No valid advertisements were found.")
    else:
        why_label = {
            "English": "Why this role matches your profile",
            "Finnish": "Miksi tämä työ sopii profiiliisi",
            "Swedish": "Varför tjänsten passar din profil",
        }[language]
        for index, job in enumerate(jobs, start=1):
            # Factual advertisement details come from the actual CSV, not the AI.
            output.append(
                f"**{index}. {job['title']}**  \n"
                f"**Employer:** {job['company'] or 'Not specified'}  \n"
                f"**Location:** {job['location'] or 'Not specified'}  \n"
                f"**Published:** {job['date'] or 'Not specified'}  \n"
                f"**Advertisement:** [View job advertisement]({job['url']})"
            )
            explanation_prompt = f"""You are CareerPilot, an AI career advisor.
The user's background and preferences:
{profile}

Explain briefly why THIS actual Finnish job advertisement was selected for that profile.
The ONLY known advertisement details are:
Job title: {job['title']}
Employer: {job['company']}
Municipality: {job['location']}
Industry: {job['industry']}

Write in {language}. Output ONLY one short paragraph (2 sentences) starting with
"{why_label}:" (translate naturally if needed).
Ground the explanation in the user's stated profile and the job title, industry or municipality.
Mention relevant interests or skills, but do not invent user qualifications.
The CSV does not contain the job description or required skills. Do NOT invent
employer requirements, hiring status, duties, or specific technologies used on this job.
Do not imply the advertisement is still open.
"""
            try:
                explanation = client.generate(explanation_prompt).strip()
                output.append(explanation or f"{why_label}: AI explanation unavailable.")
            except Exception:
                output.append(f"{why_label}: AI explanation unavailable (check Ollama).")

    footer = {

    }
    return "\n\n".join(output)
