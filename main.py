import sys
import time
import requests

API_URL = "https://api.classes.iastate.edu/api/courses/search"
DISCORD_WEBHOOK_URL = "PASTE_YOUR_WEBHOOK_URL_HERE"

POLL_INTERVAL = 30  # seconds

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://classes.iastate.edu",
    "User-Agent": "Mozilla/5.0 (ISU Seat Monitor)"
}

PAYLOAD = {
    "academicPeriodId": "ACADEMIC_PERIOD-2026Spring",
    "courseSubject": "HSPM - Hospitality Management",
    "courseNumber": "3830",
    "openSeats": False
}


def notify_discord(section, seats):
    message = (
        "**SEAT OPEN**\n"
        "**Course:** HSPM 3830\n"
        f"**Section:** {section}\n"
        f"**Unreserved Seats:** {seats}\n\n"
        "https://classes.iastate.edu/"
    )

    requests.post(
        DISCORD_WEBHOOK_URL,
        json={"content": message},
        timeout=10
    )


def check_for_open_seats():
    resp = requests.post(
        API_URL,
        json=PAYLOAD,
        headers=HEADERS,
        timeout=10
    )
    resp.raise_for_status()
    data = resp.json()

    for course in data.get("courses", []):
        for sec in course.get("sections", []):
            seats = sec.get("unreservedSeats", 0)
            section_id = sec.get("section", "unknown")

            print(f"Section {section_id}: {seats}")

            if seats > 0:
                notify_discord(section_id, seats)
                return True

    return False


def main():
    print("Monitoring ISU course seats… (Ctrl+C to stop)\n")

    while True:
        try:
            if check_for_open_seats():
                print("\nSeat opened — Discord alert sent.")
                sys.exit(0)

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("\nStopped.")
            sys.exit(0)

        except Exception as e:
            print("Error:", e)
            time.sleep(60)


if __name__ == "__main__":
    main()
