import requests
import json


url = "https://us-central1-sdp-bnb.cloudfunctions.net/messagePassing"


def post_notification(message):
    payload = json.dumps(message)
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
