import requests
import json

# API Configuration
API_KEY = "5UHdnxnBkddTWCBjqyEGNhTALq7Klc0ZZbP5xisP"
BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en"


def fetch_data(endpoint):
    """Fetch data from SportRadar API and return JSON."""
    url = BASE_URL + "/" + endpoint + ".json?api_key=" + API_KEY
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    print("Error:", response.status_code, response.text)
    return None


# Fetch & Display Competitions
competitions = fetch_data("competitions")
if competitions:
    print(json.dumps(competitions, indent=2))
else:
    print("No data received.")