import os
import openai
import requests

print("🔧 Starting slack_handler.py")

openai.api_key = os.getenv("OPENAI_API_KEY")
slack_response_url = os.getenv("SLACK_RESPONSE_URL")

print(f"🔑 OpenAI key loaded: {'Yes' if openai.api_key else 'No'}")
print(f"🌐 Slack URL: {slack_response_url}")

complaint_text = "This is a test complaint. I am not happy and want a manager."

def gpt_analyze(complaint):
    print("📡 Sending complaint to OpenAI...")
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a complaint tier classifier. Return complaint tier and explanation."},
            {"role": "user", "content": complaint}
        ],
        temperature=0.2
    )
    print("✅ OpenAI responded!")
    return response.choices[0].message.content

try:
    result = gpt_analyze(complaint_text)
    payload = {
        "response_type": "in_channel",
        "text": f"🧠 GPT Complaint Analysis:\n{result}"
    }

    print(f"📤 Sending payload to Slack/Webhook:\n{payload}")
    res = requests.post(slack_response_url, json=payload)

    print(f"✅ Sent to Slack: status={res.status_code}, response={res.text}")

except Exception as e:
    print(f"❌ Error: {e}")
