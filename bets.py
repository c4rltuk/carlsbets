import requests
import json
from datetime import datetime

API_KEY = "9d2743d4eemshce50772abe471b4p10044djsneda9425bfa9d"

URL = "https://the-racing-api1.p.rapidapi.com/v1/racecards/free"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "the-racing-api1.p.rapidapi.com"
}

PARAMS = {
    "day": "today",
    "region_codes": '["gb","ire"]'
}

def fetch_racecards():
    try:
        response = requests.get(URL, headers=HEADERS, params=PARAMS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching racecards: {e}")
        return None

def process_data(data):
    # Basic example: pick the first horse from each race
    best_bets = []

    for meeting in data.get("meetings", []):
        for race in meeting.get("races", []):
            if race.get("runners"):
                horse = race["runners"][0]  # pick first horse for now
                best_bets.append({
                    "race": race.get("race_name"),
                    "time": race.get("race_time"),
                    "course": meeting.get("course_name"),
                    "best_bet": horse.get("horse_name"),
                    "odds": horse.get("odds_decimal"),
                    "trainer": horse.get("trainer_name"),
                    "jockey": horse.get("jockey_name")
                })

    return best_bets

def save_json(best_bets, raw):
    output = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "best_bets": best_bets,
        "raw_data": raw
    }

    with open("bets.json", "w") as f:
        json.dump(output, f, indent=4)

    print("bets.json updated successfully")

def main():
    print("Fetching today's racecards...")
    data = fetch_racecards()

    if not data:
        print("No data received.")
        return

    best_bets = process_data(data)
    save_json(best_bets, data)

if __name__ == "__main__":
    main()


