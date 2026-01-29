import os
import requests
from datetime import datetime

# Secrets from GitHub Actions
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")  # group chat id or channel id

if not BOT_TOKEN or not CHANNEL:
    raise Exception("BOT_TOKEN या CHANNEL सेट नहीं है!")

# Example quiz question
quiz_question = "आज का SSC क्विज़:\n\nQ: भारत की राजधानी क्या है?\n\nA) मुंबई\nB) दिल्ली\nC) कोलकाता\nD) चेन्नई"

# Send message function
def send_quiz():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL,
        "text": quiz_question
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"Quiz sent successfully at {datetime.now()}")
    else:
        print(f"Failed to send quiz. Status code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    send_quiz()
