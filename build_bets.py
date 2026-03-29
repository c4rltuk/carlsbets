import requests
import datetime
import json
from pathlib import Path

API_BASE_URL = "https://example-racing-api.com"  # replace with real API
API_KEY = "YOUR_API_KEY_HERE"  # remove if not needed

HEADERS = {
    "Accept": "application/json",
    # "Authorization": f"Bearer {API_KEY}",
}

def get_today_iso():
    return datetime.date.today().isoformat()

def fetch_todays_races():
    date_str = get_today_iso()
    url = f"{API_BASE_URL}/races?date={date_str}&region=uk-ire"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()

def normalise(value, min_val, max_val):
    if max_val == min_val:
        return 0.5
    return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))

def compute_scores(races_json):
    horses = []

    for race in races_json.get("races", []):
        course = race.get("course_name")
        race_time = race.get("off_time")

        for runner in race.get("runners", []):
            horse_name = runner.get("horse_name")
            trainer_name = runner.get("trainer_name")
            yard_name = runner.get("yard_name", trainer_name)

            raw_horse_form = runner.get("last_3_runs_rating", 70)
            raw_trainer_sr = runner.get("trainer_strike_rate", 15)
            raw_yard_sr = runner.get("yard_strike_rate", 14)

            horse_form = normalise(raw_horse_form, 0, 100)
            trainer_form = normalise(raw_trainer_sr, 0, 30)
            yard_form = normalise(raw_yard_sr, 0, 30)

            score = (
                0.5 * horse_form +
                0.3 * trainer_form +
                0.2 * yard_form
            )

            horses.append({
                "race_time": race_time,
                "course": course,
                "horse": horse_name,
                "trainer": trainer_name,
                "yard": yard_name,
                "horse_form": round(horse_form, 3),
                "trainer_form": round(trainer_form, 3),
                "yard_form": round(yard_form, 3),
                "score": round(score, 3),
                "odds": runner.get("early_price")
            })

    horses.sort(key=lambda x: x["score"], reverse=True)
    return horses

def write_bets_json(horses, path="bets.json"):
    Path(path).write_text(json.dumps(horses, indent=2), encoding="utf-8")
    print(f"Wrote {len(horses)} horses to {path}")

def main():
    print("Fetching today’s races...")
    races_json = fetch_todays_races()
    print("Computing scores...")
    horses = compute_scores(races_json)
    print("Writing bets.json...")
    write_bets_json(horses)

if __name__ == "__main__":
    main()
