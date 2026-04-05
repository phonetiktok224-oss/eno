import csv
import os

FILE = "matches.csv"

def get_matches_csv():
    if not os.path.exists(FILE):
        return []

    matches = []

    try:
        with open(FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                matches.append({
                    "home": row.get("HomeTeam"),
                    "away": row.get("AwayTeam"),
                    "date": row.get("Date"),
                    "league": "CSV"
                })

    except Exception as e:
        print("CSV ERROR:", e)

    return matches