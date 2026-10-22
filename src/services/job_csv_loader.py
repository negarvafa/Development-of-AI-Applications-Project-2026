import csv
from pathlib import Path


def load_jobs_from_csv():
    project_root = Path(__file__).resolve().parents[2]
    file_path = project_root / "data" / "jobs-export.csv"

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        jobs = list(reader)

    return jobs

def prepare_jobs(jobs):
    prepared_jobs = []

    for job in jobs:
        prepared_jobs.append({
            "title": job["Job title"],
            "company": job["Employer"],
            "location": job["Municipality"],
            "industry": job["Industry"],
            "languages": job["Required languages"],
            "url": job["Job URL"],
        })

    return prepared_jobs

if __name__ == "__main__":
    jobs = load_jobs_from_csv()
    jobs = prepare_jobs(jobs)

    print(f"Loaded {len(jobs)} jobs")

    for job in jobs[:3]:
        print(job)