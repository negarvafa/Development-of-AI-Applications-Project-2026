"""Load and rank advertisements from the bundled Finnish job export (offline only)."""

import csv
import re
from pathlib import Path
from urllib.parse import urlparse

CSV_PATH = Path(__file__).resolve().parents[2] / "data" / "jobs-export.csv"

# Common English/Finnish equivalents. The CSV has titles, not job descriptions.
# These only improve retrieval; they are NOT assertions about a vacancy's requirements.
RELATED_TERMS = (
    {"software", "developer", "programmer", "programming", "ohjelmisto", "ohjelmistokehittäjä", "kehittäjä", "koodaus", "coding", "python", "java", "javascript", "c++", "fullstack", "backend", "frontend"},
    {"ai", "ml", "artificial", "intelligence", "machine", "learning", "tekoäly", "koneoppiminen", "pytorch", "tensorflow"},
    {"data", "analytics", "analyst", "analysis", "analyysi", "analyytikko", "tietoanalytiikka", "datascience", "scientist", "tutkimus"},
    {"cybersecurity", "security", "tietoturva", "soc", "infosec", "cyber", "kyberturva"},
    {"cloud", "devops", "pilvi", "azure", "aws", "infrastructure", "infra", "kubernetes", "platform"},
    {"network", "networks", "networking", "verkko", "tietoliikenne", "ict", "it", "information", "technology", "tietotekniikka"},
    {"embedded", "sulautettu", "electronics", "elektroniikka", "robotiikka", "robotics", "automation", "automaatio"},
    {"design", "designer", "ux", "ui", "muotoilu", "suunnittelija", "figma"},
    {"sales", "myynti", "asiakaspalvelu", "customer", "service"},
    {"finance", "financial", "talous", "kirjanpito", "accounting"},
    {"nurse", "nursing", "hoitaja", "terveydenhuolto", "healthcare", "sairaanhoitaja"},
)

STOP_WORDS = {
    "and", "for", "the", "with", "from", "this", "that", "your", "have", "years",
    "year", "work", "experience", "skills", "interest", "interests", "career", "job",
    "education", "student", "studying", "engineer", "engineering", "in", "on", "or",
    "my", "i", "to", "a", "an", "of", "as", "at", "is", "are", "want", "looking",
    "ja", "tai", "olen", "minä", "minulla", "vuotta", "haluan", "työ", "työtä",
    "kiinnostaa", "opiskelija", "kokemus", "osaaminen", "koulutus", "sekä",
}


def _tokens(text):
    return set(re.findall(r"[\w+#]+", (text or "").casefold())) - STOP_WORDS


def _expanded(tokens):
    """Add close occupational synonyms only if the user provided a related term."""
    terms = set(tokens)
    for group in RELATED_TERMS:
        if tokens & group:
            terms |= group
    return terms


def _valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def load_csv_jobs(csv_path=CSV_PATH):
    """Read the CSV using stdlib; skip incomplete entries and invalid URLs."""
    jobs = []
    with Path(csv_path).open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            title = (row.get("Job title") or "").strip()
            url = (row.get("Job URL") or "").strip()
            if not title or not _valid_url(url):
                continue
            jobs.append({
                "title": title,
                "company": (row.get("Employer") or "").strip(),
                "location": (row.get("Municipality") or "").strip(),
                "industry": (row.get("Industry") or "").strip(),
                "date": (row.get("Publication date") or "").strip(),
                "source": (row.get("Source") or "Finnish CSV").strip(),
                "url": url,
            })
    return jobs


def select_csv_jobs(education, skills, experience, interests, location="Finland", total_experience=0, limit=3, csv_path=CSV_PATH):
    """Rank known Finnish advertisements against all profile fields.

    Prioritize interests/skills and title matches; location is a tie-breaker.
    Do not treat this as a verified percentage or as evidence the vacancy is open.
    """
    interested = _tokens(interests)
    skilled = _tokens(skills)
    background = _tokens(" ".join([education or "", experience or ""]))
    strong = _expanded(interested | skilled)
    related_background = _expanded(background)
    preference = (location or "").casefold().replace(", finland", "").replace(", suomi", "").strip()
    if preference in {"finland", "suomi", "anywhere", "remote", "etätyö"}:
        preference = ""
    try:
        years = float(total_experience)
    except (TypeError, ValueError):
        years = 0

    scored = []
    for job in load_csv_jobs(csv_path):
        title = _tokens(job["title"])
        industry = _tokens(job["industry"])
        direct_title = title & (interested | skilled)
        expanded_title = title & strong
        background_title = title & related_background
        industry_hits = industry & (interested | skilled | background)
        score = (7 * len(direct_title) + 3 * len(expanded_title - direct_title)
                 + 2 * len(background_title - expanded_title)
                 + len(industry_hits))
        if preference and preference in job["location"].casefold():
            score += 2
        if years < 3 and title & {"junior", "trainee", "intern", "harjoittelija", "kesätyö", "opinnäytetyöntekijä", "junioriohjelmistokehittäjä"}:
            score += 3
        if years < 3 and title & {"senior", "principal", "staff", "lead", "johtaja", "päällikkö"}:
            score -= 5
        # Prefer well-matched roles, not just jobs in the requested city.
        scored.append((score, job))

    # Some advertisements occur more than once for neighboring municipalities.
    # Select the highest-ranked instance of each title + employer.
    scored.sort(key=lambda entry: (-entry[0], entry[1]["title"].casefold(), entry[1]["company"].casefold()))
    selected = []
    seen = set()
    for _, job in scored:
        key = job["title"].casefold()
        if key in seen:
            continue
        selected.append(job)
        seen.add(key)
        if len(selected) >= limit:
            break
    return selected
