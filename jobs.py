# Job Search Assistant
# Busqueda de oportunidades de TI en Costa Rica

SEARCHES = [
    "IT Support Costa Rica",
    "Help Desk Costa Rica",
    "Technical Support Costa Rica",
    "Desktop Support Costa Rica",
    "IT Technician Costa Rica",
    "Network Technician Costa Rica",
    "Junior Network Engineer Costa Rica",
    "CCNA Costa Rica",
]

LOCATION = "Costa Rica"

def show_searches():
    print("=== JOB SEARCH ASSISTANT ===")
    print(f"Location: {LOCATION}\n")

    for number, search in enumerate(SEARCHES, start=1):
        print(f"{number}. {search}")

if __name__ == "__main__":
    show_searches()
