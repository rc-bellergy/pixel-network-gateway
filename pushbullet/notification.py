import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PUSHBULLET_API_KEY = os.getenv('PUSHBULLET_API_KEY')

def send_push_notification(title, body):
    if not PUSHBULLET_API_KEY:
        raise ValueError("Pushbullet API key is not set")

    url = 'https://api.pushbullet.com/v2/pushes'
    headers = {
        'Access-Token': PUSHBULLET_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'note',
        'title': title,
        'body': body
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to send notification: {response.text}")
