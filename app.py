import streamlit as st
import re
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Complaint Tier Analyzer", layout="centered")
st.title("📝 Complaint Tier Analyzer")
st.markdown("Enter a customer complaint below and we'll detect the appropriate tier and explain why.")

TIER_1_PATTERNS = [
    r"\bdiscrimination\b", r"\bracist\b", r"\bprejudice\b", r"\bbias(?:ed)?\b", r"\bprofiling\b",
    r"\bdeceptive\b", r"\bfraud\b", r"\bscam\b",
    r"\bprivacy breach\b", r"\bdata breach\b",
    r"cfpb", r"ftc", r"department of financial", r"attorney is cc[’']?d", r"my lawyer is"
]

TIER_2_PATTERNS = [
    r"multiple times", r"no one.*responded", r"ignored", r"unresolved", r"ghosted",
    r"employee.*(rude|lied|unprofessional)", r"let me speak to (a )?(manager|supervisor)"
]

def get_complaint_tier(text):
    for pattern in TIER_1_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "Tier 1", f"Matched Tier 1 keyword: '{pattern}'"
    for pattern in TIER_2_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "Tier 2", f"Matched Tier 2 keyword: '{pattern}'"
    return "Tier 3", "No Tier 1 or 2 keyword matched. Defaulting to Tier 3."

def gpt_analysis(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a complaint triage assistant. Based on the user's input, determine if it belongs to Tier 1, Tier 2, or Tier 3 and explain why."},
                {"role": "user", "content": text}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error with GPT: {e}"

complaint_text = st.text_area("Paste the customer complaint here:", height=200)

if st.button("Analyze Complaint") and complaint_text:
    tier, explanation = get_complaint_tier(complaint_text)
    gpt_result = gpt_analysis(complaint_text)

    st.subheader("📊 Tier Classification")
    st.markdown(f"**Detected Tier:** {tier}")
    st.markdown(f"**Reasoning:** {explanation}")

    st.subheader("🤖 GPT Explanation")
    st.info(gpt_result)
else:
    st.markdown("\n_Results will appear after you click Analyze._")
