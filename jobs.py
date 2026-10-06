import json
import urllib.request
from datetime import datetime, timezone

REMOTIVE_API = "https://remotive.com/api/remote-jobs"
JOBICY_API = "https://jobicy.com/api/v2/remote-jobs?count=200"

KEYWORDS = [
    "it support",
    "technical support",
    "help desk",
    "helpdesk",
    "service desk",
    "desktop support",
    "it technician",
    "support technician",
    "network technician",
    "network support",
    "noc technician",
    "network administrator",
    "ccna",
]

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


def request_json(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "JobSearchAssistant/2.0",
            "Accept": "application/json"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def suitable(title, description="", category=""):
    title_lower = title.lower().strip()

    # Puestos demasiado avanzados
    excluded_titles = [
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
        "engineer iii",
    ]

    if any(word in title_lower for word in excluded_titles):
        return False

    # Puestos que NO corresponden a nuestro objetivo principal
    unrelated_titles = [
        "sales engineer",
        "pre-sales",
        "presales",
        "solutions engineer",
        "solution engineer",
        "customer success engineer",
        "technical success engineer",
        "technical consultant",
        "solutions consultant",
        "sap consultant",
        "cloud consultant",
        "software engineer",
        "developer",
        "devops",
    ]

    if any(word in title_lower for word in unrelated_titles):
        return False

    # Puestos que SÍ queremos.
    # Importante: ahora exigimos que aparezcan en el TÍTULO.
    target_titles = [
        "it support",
        "technical support",
        "tech support",
        "help desk",
        "helpdesk",
        "service desk",
        "desktop support",
        "desktop technician",
        "it technician",
        "support technician",
        "support specialist",
        "support analyst",
        "support engineer",
        "network support",
        "network technician",
        "network administrator",
        "noc technician",
        "noc analyst",
        "field technician",
        "field support",
    ]

    return any(word in title_lower for word in target_titles)


def get_remotive_jobs():
    jobs_found = []

    try:
        data = request_json(REMOTIVE_API)

        for job in data.get("jobs", []):
            title = job.get("title", "")

            if suitable(
                title,
                job.get("description", ""),
                job.get("category", "")
            ):
                jobs_found.append({
                    "title": title,
                    "company": job.get("company_name", "Unknown"),
                    "location": job.get(
                        "candidate_required_location",
                        "Remote"
                    ),
                    "type": "Remote",
                    "date": job.get("publication_date", ""),
                    "url": job.get("url", ""),
                    "source": "Remotive"
                })

    except Exception as error:
        print("Remotive error:", error)

    return jobs_found


def get_jobicy_jobs():
    jobs_found = []

    try:
        data = request_json(JOBICY_API)

        for job in data.get("jobs", []):
            title = job.get("jobTitle", "")
            industry = job.get("jobIndustry", [])

            if isinstance(industry, list):
                industry = " ".join(industry)

            if suitable(
                title,
                job.get("jobDescription", ""),
                industry
            ):
                jobs_found.append({
                    "title": title,
                    "company": job.get("companyName", "Unknown"),
                    "location": job.get("jobGeo", "Remote"),
                    "type": "Remote",
                    "date": job.get("pubDate", ""),
                    "url": job.get("url", ""),
                    "source": "Jobicy"
                })

    except Exception as error:
        print("Jobicy error:", error)

    return jobs_found


def remove_duplicates(jobs):
    unique = []
    seen = set()

    for job in jobs:
        key = (
            job["title"].lower().strip(),
            job["company"].lower().strip()
        )

        if key not in seen:
            seen.add(key)
            unique.append(job)

    return unique


def save_results(jobs):
    with open("jobs_found.md", "w", encoding="utf-8") as file:

        now = datetime.now(timezone.utc)

        file.write("# 🔎 IT Jobs Found\n\n")
        file.write(
            f"Last search: {now.strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        )

        file.write(
            "Searching IT Support, Help Desk, Desktop Support, "
            "Networking and CCNA opportunities.\n\n"
        )

        file.write(
            "**Target:** Costa Rica + Remote LATAM/Worldwide\n\n"
        )

        if not jobs:
            file.write("No matching jobs found today.\n")
            return

        file.write(
            f"## Found {len(jobs)} possible opportunities\n\n"
        )

        for number, job in enumerate(jobs[:30], start=1):

            file.write(
                f"## {number}. {job['title']}\n\n"
            )

            file.write(
                f"**Company:** {job['company']}\n\n"
            )

            file.write(
                f"**Location:** {job['location']}\n\n"
            )

            file.write(
                f"**Modality:** {job['type']}\n\n"
            )

            file.write(
                f"**Published:** {job['date']}\n\n"
            )

            file.write(
                f"**Source:** {job['source']}\n\n"
            )

            file.write(
                f"👉 [View job / Apply]({job['url']})\n\n"
            )

            file.write("---\n\n")


def main():

    print("=== IT JOB SEARCH ASSISTANT V2 ===\n")

    print("Searching Remotive...")
    remotive = get_remotive_jobs()
    print("Remotive matches:", len(remotive))

    print("Searching Jobicy...")
    jobicy = get_jobicy_jobs()
    print("Jobicy matches:", len(jobicy))

    all_jobs = remotive + jobicy
    all_jobs = remove_duplicates(all_jobs)

    print("\nTotal suitable jobs:", len(all_jobs))

    save_results(all_jobs)

    print("Results saved to jobs_found.md")


if __name__ == "__main__":
    main()
