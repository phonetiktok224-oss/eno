# =========================
# SCRAPER SOURCE (SAFE)
# =========================
import requests
from bs4 import BeautifulSoup

def get_matches_scraping():
    try:
        url = "https://www.flashscore.com.ng/football/"
        headers = {"User-Agent": "Mozilla/5.0"}

        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        matches = []

        for m in soup.select(".event__match"):
            home = m.select_one(".event__participant--home")
            away = m.select_one(".event__participant--away")

            if home and away:
                matches.append({
                    "home": home.text.strip(),
                    "away": away.text.strip(),
                    "date": "",
                    "league": "Scraped"
                })

        return matches

    except Exception as e:
        print("SCRAPER ERROR:", e)
        return []
