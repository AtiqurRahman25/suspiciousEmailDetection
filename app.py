import streamlit as st

from model import load_spam_model, load_hate_model, load_email_model
from utils import is_malicious_url

# Load models
spam_model, spam_vec = load_spam_model()
hate_model, hate_vec = load_hate_model()
email_model, email_vec = load_email_model()

def predict(model, vec, text):
    return model.predict(vec.transform([text]))[0]

st.title("🔐 Offline Cybersecurity Detector")
st.write("Detect Spam, Hate Speech, Phishing Emails & Malicious Links")

text = st.text_area("Enter your message or email:")

if st.button("Check"):
    if text:

        # 1. Phishing email
        if predict(email_model, email_vec, text) == 1:
            st.error("⚠️ Phishing Email Detected")

        # 2. Spam
        elif predict(spam_model, spam_vec, text) == 1:
            st.error("❌ Spam Message")

        # 3. Hate speech
        elif predict(hate_model, hate_vec, text) == 1:
            st.warning("⚠️ Hate Speech Detected")

        # 4. Malicious URL
        elif is_malicious_url(text):
            st.warning("⚠️ Malicious Link Detected")

        else:
            st.success("✅ Safe Message")