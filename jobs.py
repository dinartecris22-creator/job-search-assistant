import json
import urllib.request
from datetime import datetime

API_URL = "https://remotive.com/api/remote-jobs"

# Puestos relacionados con tu perfil
KEYWORDS = [
    "it support",
    "technical support",
    "help desk",
    "service desk",
    "desktop support",
    "it technician",
    "network technician",
    "network support",
    "network administrator",
    "noc technician",
    "ccna",
]

# Puestos que queremos evitar
EXCLUDED = [
    "senior",
    "sr.",
    "sr ",
    "lead",
    "manager",
    "director",
    "principal",
    "tier iii",
    "tier 3",
    "level iii",
    "level 3",
]


def get_jobs():
    request = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "JobSearchAssistant/1.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data["jobs"]


def matches_profile(job):
    title = job.get("title", "").lower()

    text = (
        job.get("title", "") + " " +
        job.get("description", "") + " " +
        job.get("category", "")
    ).lower()

    # Rechazar puestos avanzados
    if any(word in title for word in EXCLUDED):
        return False

    # Aceptar puestos relacionados con tu perfil
    return any(keyword in text for keyword in KEYWORDS)


def save_results(matches):
    filename = "jobs_found.md"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("# 🔎 IT Jobs Found\n\n")
        file.write(
            f"Last search: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        )

        file.write(
            "Focused on IT Support, Help Desk, Desktop Support "
            "and Networking opportunities.\n\n"
        )

        if not matches:
            file.write("No matching jobs found today.\n")
            return

        file.write(f"## Found {len(matches)} possible opportunities\n\n")

        for number, job in enumerate(matches[:20], start=1):
            title = job.get("title", "Unknown position")
            company = job.get("company_name", "Unknown company")
            location = job.get(
                "candidate_required_location",
                "Not specified"
            )
            date = job.get("publication_date", "Not specified")
            url = job.get("url", "#")

            file.write(f"## {number}. {title}\n\n")
            file.write(f"**Company:** {company}\n\n")
            file.write(f"**Location:** {location}\n\n")
            file.write(f"**Published:** {date}\n\n")
            file.write(f"👉 [Apply here]({url})\n\n")
            file.write("Source: Remotive\n\n")
            file.write("---\n\n")


def main():
    print("=== IT JOB SEARCH ASSISTANT ===")
    print("Searching for suitable IT opportunities...\n")

    jobs = get_jobs()

    matches = [
        job for job in jobs
        if matches_profile(job)
    ]

    print(f"Found {len(matches)} suitable jobs.")

    for job in matches[:20]:
        print(
            job.get("title"),
            "-",
            job.get("company_name")
        )

    save_results(matches)

    print("\nResults saved to jobs_found.md")


if __name__ == "__main__":
    main()
