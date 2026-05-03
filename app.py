import streamlit as st

from model import load_spam_model, load_hate_model, load_email_model
from utils import is_malicious_url

# Load models
spam_model, spam_vec = load_spam_model()
hate_model, hate_vec = load_hate_model()
email_model, email_vec = load_email_model()

def predict(model, vec, text):
    return model.predict(vec.transform([text]))[0]

def mask_text(text):
    return "*" * len(text)

st.set_page_config(page_title="Cybersecurity Detector", page_icon="🔐")

st.title("🔐 Offline Message Security System")
st.write("Detect Spam | Hate Speech | Phishing | Malicious Links")

message = st.text_area("Enter message:")

if st.button("Check Message"):

    if message.strip() == "":
        st.warning("Please enter a message.")
    else:

        # 1. Phishing Email
        if predict(email_model, email_vec, message) == 1:
            st.error("⚠️ Phishing Email Detected")
            st.code(mask_text(message))

        # 2. Spam
        elif predict(spam_model, spam_vec, message) == 1:
            st.error("❌ Spam Message Detected")
            st.code(mask_text(message))

        # 3. Hate Speech
        elif predict(hate_model, hate_vec, message) == 1:
            st.error("⚠️ Hate Speech Detected")
            st.code(mask_text(message))

        # 4. Malicious URL
        elif is_malicious_url(message):
            st.error("⚠️ Malicious Link Detected")
            st.code(mask_text(message))

        # 5. Safe message
        else:
            st.success("✅ Safe Message")
            st.write(message)