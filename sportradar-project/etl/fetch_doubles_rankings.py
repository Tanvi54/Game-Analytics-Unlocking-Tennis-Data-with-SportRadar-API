import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SPORTRADAR_API_KEY")

BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"

def fetch_doubles_rankings():
    url = f"{BASE_URL}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("✅ Doubles competitor rankings fetched:",
              len(data.get("rankings", [])))

        os.makedirs("sample_json", exist_ok=True)

        with open("sample_json/doubles_rankings.json", "w") as f:
            json.dump(data, f, indent=2)

        return data
    else:
        print("❌ Error:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    fetch_doubles_rankings()
