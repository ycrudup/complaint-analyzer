import os
import openai
import requests

# Load keys from GitHub Actions secrets
openai.api_key = os.getenv("OPENAI_API_KEY")
slack_response_url = os.getenv("SLACK_RESPONSE_URL")

# Replace this with real Slack input later
complaint_text = "I'm really upset. I've contacted support three times and will pursue legal options if not resolved."

# Call GPT to analyze the complaint
def gpt_analyze(complaint):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a complaint tier classifier. Return complaint tier and explanation."},
            {"role": "user", "content": complaint}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

# Format and send result back to Slack
result = gpt_analyze(complaint_text)

payload = {
    "response_type": "in_channel",
    "text": f"🧠 GPT Complaint Analysis:\n{result}"
}

res = requests.post(slack_response_url, json=payload)

if res.status_code == 200:
    print("✅ Posted to Slack successfully.")
else:
    print(f"❌ Failed to post to Slack: {res.status_code} — {res.text}")
