import json

from pathlib import Path

def load_jobs():
    file_path = Path(__file__).parent / "jobs.json"

    with open(file_path, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    return jobs

def calculate_skill_match(user_skills, job_skills):

    user_skills = {skill.lower().strip() for skill in user_skills}
    job_skills = {skill.lower().strip() for skill in job_skills}

    matching_skills = user_skills.intersection(job_skills)
    missing_skills = job_skills.difference(user_skills)

    if not job_skills:
        return 0, [], []

    score = len(matching_skills) / len(job_skills) * 100

    return round(score), sorted(matching_skills), sorted(missing_skills)

def calculate_experience_match(user_experience, required_experience):

    if required_experience == 0:
        return 100

    if user_experience >= required_experience:
        return 100

    score = user_experience / required_experience * 100

    return round(score)

def calculate_location_match(user_location, job_location):

    user_location = user_location.lower().strip()
    job_location = job_location.lower().strip()

    if user_location == job_location:
        return 100

    return 0

def rank_jobs(user_skills, user_experience, user_location, jobs):

    results = []

    for job in jobs:

        skill_score, matching_skills, missing_skills = calculate_skill_match(
            user_skills,
            job["skills"]
        )

        experience_score = calculate_experience_match(
            user_experience,
            job["experience"]
        )

        location_score = calculate_location_match(
            user_location,
            job["location"]
        )

        overall_score = (
            skill_score * 0.7 +
            experience_score * 0.2 +
            location_score * 0.1
        )


        overall_score = round(overall_score)

        results.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "score": overall_score,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "location_score": location_score,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills
        })

    # Rank the jobs from best to worst.
    results.sort(
        key=lambda job: job["score"],
        reverse=True
    )

    return results

if __name__ == "__main__":

    jobs = load_jobs()

    user_skills = [
        "Python",
        "Git",
        "Machine Learning",
        "PyTorch"
    ]

    user_experience = 1
    user_location = "Helsinki"

    results = rank_jobs(
    user_skills,
    user_experience,
    user_location,
    jobs
    )

    print("\nCareerPilot Job Recommendations\n")

    for job in results[:5]:
        print(f"{job['title']} - {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Overall match: {job['score']}%")
        print(f"Skill match: {job['skill_score']}%")
        print(f"Experience match: {job['experience_score']}%")
        print(f"Location match: {job['location_score']}%")
        print(f"Matching skills: {', '.join(job['matching_skills'])}")
        print(f"Missing skills: {', '.join(job['missing_skills'])}")
        print()