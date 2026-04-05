# =========================
# DATA SOURCES MANAGER
# =========================

from .api_source import get_matches_api
from .scraper_source import get_matches_scraping
from .csv_source import get_matches_csv

# =========================
# REMOVE DOUBLONS
# =========================
def remove_duplicates(matches):
    seen = set()
    unique = []

    for m in matches:
        key = (m.get("home"), m.get("away"), m.get("date"))

        if key not in seen:
            seen.add(key)
            unique.append(m)

    return unique

# =========================
# MAIN FUNCTION (IMPORTANT)
# =========================
def get_all_matches():
    all_matches = []

    for source in [
        get_matches_api,
        get_matches_scraping,
        get_matches_csv
    ]:
        try:
            data = source()
            if data:
                all_matches.extend(data)
        except Exception as e:
            print("SOURCE ERROR:", e)
            continue

    return remove_duplicates(all_matches)
