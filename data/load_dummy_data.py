import json
import requests

API_URL = "http://localhost:8000/events/"

def load_data():
    with open("data/sample_events.json") as f:
        events = json.load(f)
    for ev in events:
        resp = requests.post(API_URL, json=ev)
        if resp.status_code == 200:
            print(f"✅ Published {ev['order_id']}")
        else:
            print(f"❌ Failed {ev['order_id']}: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    load_data()
