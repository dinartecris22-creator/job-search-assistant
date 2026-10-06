import json
import urllib.request
from datetime import datetime, timezone


# =========================================================
# JOB SEARCH ASSISTANT V3
# Costa Rica + Remote LATAM / Worldwide
# =========================================================

REMOTIVE_API = "https://remotive.com/api/remote-jobs"

JOBICY_API = (
    "https://jobicy.com/api/v2/remote-jobs?count=200"
)


# =========================================================
# TITULOS QUE QUEREMOS ENCONTRAR
# =========================================================

TARGET_TITLES = [
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


# =========================================================
# PUESTOS AVANZADOS QUE NO QUEREMOS
# =========================================================

EXCLUDED_TITLES = [
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


# =========================================================
# PUESTOS QUE PRODUCIAN FALSOS POSITIVOS
# =========================================================

UNRELATED_TITLES = [
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


# =========================================================
# DESCARGAR JSON DESDE UNA API
# =========================================================

def request_json(url):

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "JobSearchAssistant/3.0",
            "Accept": "application/json",
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=30
    ) as response:

        return json.loads(
            response.read().decode("utf-8")
        )


# =========================================================
# FILTRO DE PUESTOS
# =========================================================

def suitable(title):

    title_lower = title.lower().strip()

    # Eliminar puestos avanzados
    if any(
        word in title_lower
        for word in EXCLUDED_TITLES
    ):
        return False

    # Eliminar puestos que no corresponden
    if any(
        word in title_lower
        for word in UNRELATED_TITLES
    ):
        return False

    # El titulo debe coincidir con nuestro perfil
    return any(
        word in title_lower
        for word in TARGET_TITLES
    )


# =========================================================
# REMOTIVE
# =========================================================

def get_remotive_jobs():

    jobs_found = []

    try:

        data = request_json(REMOTIVE_API)

        for job in data.get("jobs", []):

            title = job.get("title", "")

            if suitable(title):

                jobs_found.append({
                    "title": title,

                    "company": job.get(
                        "company_name",
                        "Unknown"
                    ),

                    "location": job.get(
                        "candidate_required_location",
                        "Remote"
                    ),

                    "type": "Remote",

                    "date": job.get(
                        "publication_date",
                        ""
                    ),

                    "url": job.get(
                        "url",
                        ""
                    ),

                    "source": "Remotive",
                })

    except Exception as error:

        print(
            "Remotive error:",
            error
        )

    return jobs_found


# =========================================================
# JOBICY
# =========================================================

def get_jobicy_jobs():

    jobs_found = []

    try:

        data = request_json(JOBICY_API)

        for job in data.get("jobs", []):

            title = job.get(
                "jobTitle",
                ""
            )

            if suitable(title):

                jobs_found.append({
                    "title": title,

                    "company": job.get(
                        "companyName",
                        "Unknown"
                    ),

                    "location": job.get(
                        "jobGeo",
                        "Remote"
                    ),

                    "type": "Remote",

                    "date": job.get(
                        "pubDate",
                        ""
                    ),

                    "url": job.get(
                        "url",
                        ""
                    ),

                    "source": "Jobicy",
                })

    except Exception as error:

        print(
            "Jobicy error:",
            error
        )

    return jobs_found


# =========================================================
# ELIMINAR DUPLICADOS
# =========================================================

def remove_duplicates(jobs):

    unique = []
    seen = set()

    for job in jobs:

        key = (
            job["title"].lower().strip(),
            job["company"].lower().strip(),
        )

        if key not in seen:

            seen.add(key)

            unique.append(job)

    return unique


# =========================================================
# GUARDAR RESULTADOS
# =========================================================

def save_results(jobs):

    with open(
        "jobs_found.md",
        "w",
        encoding="utf-8"
    ) as file:

        now = datetime.now(timezone.utc)

        file.write(
            "# 🔎 IT Jobs Found\n\n"
        )

        file.write(
            f"Last search: "
            f"{now.strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        )

        file.write(
            "Searching IT Support, Help Desk, "
            "Desktop Support, Networking and "
            "CCNA opportunities.\n\n"
        )

        file.write(
            "**Target:** Costa Rica - Onsite / Hybrid / Remote "
            "+ Remote LATAM / Worldwide\n\n"
        )


        # =================================================
        # COSTA RICA
        # =================================================

        file.write(
            "# 🇨🇷 Costa Rica - Local Job Searches\n\n"
        )

        file.write(
            "Searches for onsite, hybrid and remote "
            "opportunities in Costa Rica.\n\n"
        )


        # LINKEDIN

        file.write(
            "## LinkedIn\n\n"
        )

        file.write(
            "👉 [IT Support Costa Rica]"
            "(https://www.linkedin.com/jobs/search/"
            "?keywords=IT%20Support&location=Costa%20Rica)\n\n"
        )

        file.write(
            "👉 [Help Desk Costa Rica]"
            "(https://www.linkedin.com/jobs/search/"
            "?keywords=Help%20Desk&location=Costa%20Rica)\n\n"
        )

        file.write(
            "👉 [Service Desk Costa Rica]"
            "(https://www.linkedin.com/jobs/search/"
            "?keywords=Service%20Desk&location=Costa%20Rica)\n\n"
        )

        file.write(
            "👉 [Desktop Support Costa Rica]"
            "(https://www.linkedin.com/jobs/search/"
            "?keywords=Desktop%20Support&location=Costa%20Rica)\n\n"
        )

        file.write(
            "👉 [Technical Support Costa Rica]"
            "(https://www.linkedin.com/jobs/search/"
            "?keywords=Technical%20Support&location=Costa%20Rica)\n\n"
        )

        file.write(
            "👉 [Network Technician Costa Rica]"
            "(https://www.linkedin.com/jobs/search/"
            "?keywords=Network%20Technician&location=Costa%20Rica)\n\n"
        )

        file.write(
            "👉 [NOC Costa Rica]"
            "(https://www.linkedin.com/jobs/search/"
            "?keywords=NOC&location=Costa%20Rica)\n\n"
        )


        # INDEED

        file.write(
            "## Indeed Costa Rica\n\n"
        )

        file.write(
            "👉 [IT Support]"
            "(https://cr.indeed.com/jobs"
            "?q=IT+Support&l=Costa+Rica)\n\n"
        )

        file.write(
            "👉 [Help Desk]"
            "(https://cr.indeed.com/jobs"
            "?q=Help+Desk&l=Costa+Rica)\n\n"
        )

        file.write(
            "👉 [Service Desk]"
            "(https://cr.indeed.com/jobs"
            "?q=Service+Desk&l=Costa+Rica)\n\n"
        )

        file.write(
            "👉 [Technical Support]"
            "(https://cr.indeed.com/jobs"
            "?q=Technical+Support&l=Costa+Rica)\n\n"
        )

        file.write(
            "👉 [Desktop Support]"
            "(https://cr.indeed.com/jobs"
            "?q=Desktop+Support&l=Costa+Rica)\n\n"
        )

        file.write(
            "👉 [Network Technician]"
            "(https://cr.indeed.com/jobs"
            "?q=Network+Technician&l=Costa+Rica)\n\n"
        )

        file.write(
            "---\n\n"
        )


        # =================================================
        # RESULTADOS AUTOMATICOS
        # =================================================

        file.write(
            "# 🌎 Automatically Found Jobs\n\n"
        )

        file.write(
            "Sources: Jobicy + Remotive\n\n"
        )

        if not jobs:

            file.write(
                "No matching automatic jobs "
                "found today.\n"
            )

            return


        file.write(
            f"## Found {len(jobs)} "
            "possible opportunities\n\n"
        )


        for number, job in enumerate(
            jobs[:30],
            start=1
        ):

            file.write(
                f"## {number}. "
                f"{job['title']}\n\n"
            )

            file.write(
                f"**Company:** "
                f"{job['company']}\n\n"
            )

            file.write(
                f"**Location:** "
                f"{job['location']}\n\n"
            )

            file.write(
                f"**Modality:** "
                f"{job['type']}\n\n"
            )

            file.write(
                f"**Published:** "
                f"{job['date']}\n\n"
            )

            file.write(
                f"**Source:** "
                f"{job['source']}\n\n"
            )

            file.write(
                f"👉 [View job / Apply]"
                f"({job['url']})\n\n"
            )

            file.write(
                "---\n\n"
            )


# =========================================================
# EJECUTAR ASISTENTE
# =========================================================

def main():

    print(
        "=== IT JOB SEARCH ASSISTANT V3 ===\n"
    )

    print(
        "Searching Remotive..."
    )

    remotive = get_remotive_jobs()

    print(
        "Remotive matches:",
        len(remotive)
    )


    print(
        "Searching Jobicy..."
    )

    jobicy = get_jobicy_jobs()

    print(
        "Jobicy matches:",
        len(jobicy)
    )


    all_jobs = (
        remotive +
        jobicy
    )

    all_jobs = remove_duplicates(
        all_jobs
    )


    print(
        "\nTotal suitable jobs:",
        len(all_jobs)
    )


    save_results(
        all_jobs
    )


    print(
        "\nResults saved to jobs_found.md"
    )


if __name__ == "__main__":
    main()
