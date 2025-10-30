import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SPORTRADAR_API_KEY")

BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json"

def fetch_competitions():
    url = f"{BASE_URL}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("✅ Competitions fetched:", len(data.get("competitions", [])))

        # ✅ Create folder if it doesn't exist
        os.makedirs("sample_json", exist_ok=True)

        # ✅ Save JSON data for debugging
        with open("sample_json/competitions.json", "w") as f:
            json.dump(data, f, indent=2)

        return data
    else:
        print("❌ Error:", response.status_code, response.text)

if __name__ == "__main__":
    data = fetch_competitions()
