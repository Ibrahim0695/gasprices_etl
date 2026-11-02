import http.client
import json
import os

from dotenv import load_dotenv

load_dotenv()

def extract_prices():
    api_key = os.getenv("COLLECTAPI_KEY")
    if not api_key:
        raise RuntimeError("COLLECTAPI_KEY must be set in the environment or .env file.")

    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        "content-type": "application/json",
        "authorization": f"apikey {api_key}",
    }

    try:
        conn.request("GET", "/gasPrice/stateUsaPrice?state=WA", headers=headers)

        response = conn.getresponse()
        data = response.read()
    finally:
        conn.close()

    return json.loads(data.decode("utf-8"))