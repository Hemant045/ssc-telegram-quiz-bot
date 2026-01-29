import os
import requests
import json
from datetime import datetime

# Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")

if not BOT_TOKEN or not CHANNEL:
    raise Exception("BOT_TOKEN या CHANNEL सेट नहीं है!")

# Example quiz question and options
quiz_question = "भारत की राजधानी क्या है?"
quiz_options = ["मुंबई", "दिल्ली", "कोलकाता", "चेन्नई"]

def send_quiz_poll():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"
    
    payload = {
        "chat_id": CHANNEL,
        "question": quiz_question,
        "options": json.dumps(quiz_options),  # ✅ Proper JSON string
        "is_anonymous": False
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"Quiz poll sent successfully at {datetime.now()}")
    else:
        print(f"Failed to send quiz poll. Status code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    send_quiz_poll()
