import json
import urllib.request

API_URL = "https://remotive.com/api/remote-jobs"

KEYWORDS = [
    "it support",
    "technical support",
    "help desk",
    "service desk",
    "desktop support",
    "it technician",
    "network technician",
    "network support",
    "ccna",
]

def get_jobs():
    request = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "JobSearchAssistant/1.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))["jobs"]


def matches_profile(job):
    text = (
        job.get("title", "") + " " +
        job.get("description", "") + " " +
        job.get("category", "")
    ).lower()

    return any(keyword in text for keyword in KEYWORDS)


def main():
    print("=== IT JOB SEARCH ASSISTANT ===")
    print("Searching for remote IT opportunities...\n")

    jobs = get_jobs()
    matches = [job for job in jobs if matches_profile(job)]

    if not matches:
        print("No matching jobs found today.")
        return

    print(f"Found {len(matches)} possible jobs:\n")

    for job in matches[:20]:
        print("=" * 60)
        print("POSITION:", job.get("title"))
        print("COMPANY:", job.get("company_name"))
        print("LOCATION:", job.get("candidate_required_location"))
        print("DATE:", job.get("publication_date"))
        print("APPLY:", job.get("url"))
        print("SOURCE: Remotive")


if __name__ == "__main__":
    main()
