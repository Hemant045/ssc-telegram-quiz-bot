import os
import json
import requests
from datetime import date
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


# ------------------ Generate Quiz ------------------
def generate_quiz():
    today = date.today().strftime("%d %B %Y")

    prompt = f"""
Create 5 SSC-level multiple choice CURRENT AFFAIRS questions
strictly based on events around {today}.

Rules:
- Each question must be different
- Topics: Government schemes, sports, awards, economy, defence
- Language: Hindi
- 4 options per question
- Clearly mention correct answer index (0-based)

Output format (JSON only):
[
  {{
    "question": "...",
    "options": ["A","B","C","D"],
    "correct": 1
  }}
]
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )

    raw = response.choices[0].message.content.strip()

    # 🔴 SAFETY: JSON extract
    raw = raw[raw.find("["): raw.rfind("]") + 1]

    return json.loads(raw)


# ------------------ Send Quiz Poll ------------------
def send_quiz_poll(question, options, correct):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"

    payload = {
        "chat_id": CHANNEL,
        "question": question,
        "options": json.dumps(options),
        "type": "quiz",                  # 🔴 MUST
        "correct_option_id": correct,    # 🔴 MUST
        "is_anonymous": True
    }

    response = requests.post(url, data=payload)
    print("Telegram response:", response.text)


# ------------------ MAIN ------------------
if __name__ == "__main__":
    quiz_list = generate_quiz()

    for quiz in quiz_list:
        send_quiz_poll(
            quiz["question"],
            quiz["options"],
            quiz["correct"]
        )
