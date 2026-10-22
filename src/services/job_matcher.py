import csv

import json

from pathlib import Path

from src.services.job_csv_loader import load_jobs_from_csv, prepare_jobs

# Load job data from the JSON file.
def load_jobs():
    file_path = Path(__file__).parent / "jobs.json"

    with open(file_path, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    return jobs

# Load job data from the CSV dataset.
def load_jobs_from_csv():
    file_path = Path(__file__).parent.parent.parent / "data" / "jobs-export.csv"

    jobs = []

    with open(file_path, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            jobs.append(row)

    return jobs

# Compare the user's skills with the skills required for the job
# Return the match percentage, matching skills, and missing skills.
def calculate_skill_match(user_skills, job_skills):

    user_skills = {skill.lower().strip() for skill in user_skills}
    job_skills = {skill.lower().strip() for skill in job_skills}

    matching_skills = user_skills.intersection(job_skills)
    missing_skills = job_skills.difference(user_skills)

    if not job_skills:
        return 0, [], []

    score = len(matching_skills) / len(job_skills) * 100

    return round(score), sorted(matching_skills), sorted(missing_skills)

# Calculate how well the user's work experience meets the job requirement.
def calculate_experience_match(user_experience, required_experience):

    if required_experience == 0:
        return 100

    if user_experience >= required_experience:
        return 100

    score = user_experience / required_experience * 100

    return round(score)

# Check whether the job location matches the user's preferred location.
# Remote jobs are considered suitable regardless of the user's location.
def calculate_location_match(user_location, job_location):

    user_location = user_location.lower().strip()
    job_location = job_location.lower().strip()

    if user_location == job_location:
        return 100

    if job_location == "remote":
        return 100

    return 0

# Calculate the overall match score for each job and rank jobs.
# from the best match to the lowest match.
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

# Calculate the overall score using weighted matching criteria:
# skills 70%, experience 20%, and location 10%.
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


# # Test the job matching functionality with a sample user profile.
# if __name__ == "__main__":

#     csv_jobs = load_jobs_from_csv()

#     print(f"Loaded {len(csv_jobs)} jobs from CSV")
#     print(csv_jobs[0])

#     jobs = load_jobs()

#     # vanha testikoodi jatkuu...

#     jobs = load_jobs()

#     user_skills = [
#         "Python",
#         "Git",
#         "Machine Learning",
#         "PyTorch"
#     ]

#     user_experience = 1
#     user_location = "Helsinki"

#     results = rank_jobs(
#     user_skills,
#     user_experience,
#     user_location,
#     jobs
#     )

#     print("\nCareerPilot Job Recommendations\n")

#     for job in results[:5]:
#         print(f"{job['title']} - {job['company']}")
#         print(f"Location: {job['location']}")
#         print(f"Overall match: {job['score']}%")
#         print(f"Skill match: {job['skill_score']}%")
#         print(f"Experience match: {job['experience_score']}%")
#         print(f"Location match: {job['location_score']}%")
#         print(f"Matching skills: {', '.join(job['matching_skills'])}")
#         print(f"Missing skills: {', '.join(job['missing_skills'])}")
#         print()

def rank_csv_jobs(user_location, user_interests, jobs):

    results = []

    location = user_location.lower().strip()
    interests = [
        interest.lower().strip()
        for interest in user_interests
    ]

    for job in jobs:

        score = 0

        job_location = job["location"].lower().strip()
        job_title = job["title"].lower()
        job_industry = job["industry"].lower()

        # Location match
        if location and location == job_location:
            score += 40

        # Interest match
        matching_interests = []

        for interest in interests:
            if interest in job_title or interest in job_industry:
                score += 20
                matching_interests.append(interest)

        results.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "industry": job["industry"],
            "languages": job["languages"],
            "url": job["url"],
            "score": score,
            "matching_interests": matching_interests,
        })

    results.sort(
        key=lambda job: job["score"],
        reverse=True
    )

    return results

if __name__ == "__main__":

    jobs = load_jobs_from_csv()
    jobs = prepare_jobs(jobs)

    user_location = "Helsinki"

    user_interests = [
        "software",
        "data",
        "technology"
    ]

    results = rank_csv_jobs(
        user_location,
        user_interests,
        jobs
    )

    print("\nCareerPilot Real Job Recommendations\n")

    for job in results[:10]:
        print(f"{job['title']} - {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Industry: {job['industry']}")
        print(f"Match score: {job['score']}")
        print(f"URL: {job['url']}")
        print()