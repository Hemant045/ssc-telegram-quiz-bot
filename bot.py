import os
import requests
import json
import openai
from datetime import datetime

# Secrets from GitHub
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")
OPENAI_KEY = os.getenv("OPENAI_KEY")

if not BOT_TOKEN or not CHANNEL or not OPENAI_KEY:
    raise Exception("BOT_TOKEN, CHANNEL या OPENAI_KEY missing! Add them in repo secrets.")

openai.api_key = OPENAI_KEY

# Function to generate 5 current affairs SSC questions
def generate_quiz():
    prompt = """Generate 5 current affairs multiple choice questions for SSC exam.
    Format: question, 4 options (A-D), correct answer index (0-3)
    Return in JSON array format: [{"question": "...", "options": ["...","...","...","..."], "answer": 1}, ...]
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    try:
        quiz_data = json.loads(response.choices[0].message.content)
        return quiz_data
    except Exception as e:
        print("Error parsing OpenAI response:", e)
        return []

# Function to send quiz poll to Telegram
def send_quiz_poll(question, options, correct_option_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"
    payload = {
        "chat_id": CHANNEL,
        "question": question,
        "options": json.dumps(options),
        "type": "quiz",
        "correct_option_id": correct_option_id,
        "is_anonymous": True  # required for channel
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"✅ Quiz sent successfully at {datetime.now()}")
    else:
        print(f"❌ Failed to send quiz. Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    quiz_list = generate_quiz()
    for q in quiz_list:
        send_quiz_poll(q['question'], q['options'], q['answer'])
