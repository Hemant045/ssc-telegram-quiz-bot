import os
from datetime import date
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

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
        temperature=0.9  # 🔥 randomness
    )

    return json.loads(response.choices[0].message.content)
