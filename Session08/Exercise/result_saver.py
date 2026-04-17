import json
import os
from datetime import datetime


class ResultSaver:
    def __init__(self, filepath="country_results.json"):
        self.filepath = filepath

    def _load_existing(self):
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    def save(self, search_term, result):
        if not result:
            print("[ResultSaver] Nothing to save.")
            return

        country = result[0]

        record = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "search_term": search_term,
            "country": country.get("name", {}).get("common", "N/A"),
            "official_name": country.get("name", {}).get("official", "N/A"),
            "capital": country.get("capital", ["N/A"])[0],
            "region": country.get("region", "N/A"),
            "subregion": country.get("subregion", "N/A"),
            "population": country.get("population", "N/A"),
        }

        existing_data = self._load_existing()
        existing_data.append(record)

        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=2, ensure_ascii=False)

        print(f"[ResultSaver] Saved to {self.filepath} ({len(existing_data)} record(s) total)")
        print(f"Result saved at {record['timestamp']}")