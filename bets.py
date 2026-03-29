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
    url = f"{API_BASE_URL}/racecards"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error fetching racecards:", e)
        return None


def score_horse(horse):
    """Simple scoring model for best‑bet selection."""
    score = 0

    # 1. Betting position (if odds exist)
    if "odds_position" in horse and horse["odds_position"]:
        if horse["odds_position"] <= 3:
            score += 3

    # 2. Recent form
    if "form" in horse and horse["form"]:
        if any(ch in horse["form"][:3] for ch in ["1", "2"]):
            score += 2

    # 3. Trainer quality
    if horse.get("trainer_rating", 0) >= 4:
        score += 1

    # 4. Jockey quality
    if horse.get("jockey_rating", 0) >= 4:
        score += 1

    return score


def pick_best_bets(racecards):
    best_bets = []

    for race in racecards.get("races", []):
        horses = race.get("horses", [])
        if not horses:
            continue

        # Score each horse
        for horse in horses:
            horse["score"] = score_horse(horse)

        # Pick the top‑scoring horse
        best = max(horses, key=lambda h: h["score"])

        best_bets.append({
            "race": race.get("race_name"),
            "time": race.get("race_time"),
            "course": race.get("course"),
            "best_bet": best.get("name"),
            "score": best.get("score"),
            "odds": best.get("odds"),
            "trainer": best.get("trainer"),
            "jockey": best.get("jockey"),
        })

    return best_bets


def save_bets_to_file(data):
    try:
        with open("bets.json", "w") as f:
            json.dump(data, f, indent=4)
        print("bets.json updated successfully")
    except Exception as e:
        print("Error writing bets.json:", e)


def main():
    print("Fetching today's racecards...")

    racecards = get_today_racecards()
    if not racecards:
        print("No data received.")
        return

    best_bets = pick_best_bets(racecards)

    output = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "best_bets": best_bets,
        "raw_data": racecards
    }

    save_bets_to_file(output)


if __name__ == "__main__":
    main()

