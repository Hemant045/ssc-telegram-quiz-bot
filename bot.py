import os
import requests
from datetime import datetime

# Secrets from GitHub Actions
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")  # group chat id or channel id

if not BOT_TOKEN or not CHANNEL:
    raise Exception("BOT_TOKEN या CHANNEL सेट नहीं है!")

# Quiz question and options
quiz_question = "भारत की राजधानी क्या है?"
quiz_options = ["मुंबई", "दिल्ली", "कोलकाता", "चेन्नई"]

# Send poll function
def send_quiz_poll():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"
    payload = {
        "chat_id": CHANNEL,
        "question": quiz_question,
        "options": str(quiz_options),  # must be JSON array as string
        "is_anonymous": False  # अगर true रखा तो votes anonymous रहेंगे
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"Quiz poll sent successfully at {datetime.now()}")
    else:
        print(f"Failed to send quiz poll. Status code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    send_quiz_poll()
