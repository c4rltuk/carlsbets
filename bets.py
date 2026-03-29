import requests
import json
from datetime import datetime

API_KEY = "9d2743d4eemshce50772abe471b4p10044djsneda9425bfa9d"

API_BASE_URL = "https://racing-api1.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "racing-api1.p.rapidapi.com"
}

def get_today_racecards():
    """Fetch today's racecards from the Racing API."""
    url = f"{API_BASE_URL}/racecards"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print("Error fetching racecards:", e)
        return None


def save_bets_to_file(data):
    """Save race data to bets.json."""
    try:
        with open("bets.json", "w") as f:
            json.dump(data, f, indent=4)
        print("bets.json updated successfully")

    except Exception as e:
        print("Error writing bets.json:", e)


def main():
    print("Fetching today's racecards...")

    racecards = get_today_racecards()

    if racecards is None:
        print("No data received. Exiting.")
        return

    # Add timestamp for clarity
    output = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "racecards": racecards
    }

    save_bets_to_file(output)


if __name__ == "__main__":
    main()
