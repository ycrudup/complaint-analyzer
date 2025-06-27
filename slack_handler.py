import os
import openai
import requests
import urllib.parse

# 🔐 Load OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🔍 Load Slack payload from test string (replace this with actual GitHub Actions input handling later)
payload_raw = """token=tdVJO0C6NzAzaoOB3z1ly0tW&team_id=T05HJ0CKWG5&team_domain=sq-block&channel_id=D088BM5QL5Q&channel_name=directmessage&user_id=U0888S0R9SR&user_name=066953&command=%2Fcomplaint&text=This+is+a+test+complaint&api_app_id=A093B23SNS0&is_enterprise_install=false&enterprise_id=E01BAFDEXUP&enterprise_name=Block%2C+Inc.&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT05HJ0CKWG5%2F9098225233767%2FF2Hf86PxdUWNcAL4QXibMLae&trigger_id=9098225241191.5596012676549.5e2ba9bc1598fb5738f5d4f2c91368cd"""

# Parse Slack's x-www-form-urlencoded body
payload = urllib.parse.parse_qs(payload_raw)

# 🔍 Extract complaint and response URL
complaint_text = payload['text'][0]
slack_response_url = payload['response_url'][0]

print(f"📨 Complaint: {complaint_text}")
print(f"🌐 Slack response URL: {slack_response_url}")

# 🔁 GPT Analysis
def gpt_analyze(complaint):
    print("📡 Sending to OpenAI...")
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a complaint tier classifier. Return complaint tier and explanation."},
            {"role": "user", "content": complaint}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

try:
    result = gpt_analyze(complaint_text)
    payload = {
        "response_type": "in_channel",
        "text": f"🧠 GPT Complaint Analysis:\n{result}"
    }

    res = requests.post(slack_response_url, json=payload)

    print(f"✅ Posted to Slack: {res.status_code} | {res.text}")

except Exception as e:
    print(f"❌ Error: {e}")

