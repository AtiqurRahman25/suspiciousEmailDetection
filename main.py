from model import load_spam_model, load_hate_model, load_email_model
from utils import is_malicious_url

# Load models
spam_model, spam_vec = load_spam_model()
hate_model, hate_vec = load_hate_model()
email_model, email_vec = load_email_model()

# Generic prediction function
def predict(model, vec, text):
    return model.predict(vec.transform([text]))[0]

# ✅ Domain safety override (fixes false spam like university text)
def safe_override(text):
    text = text.lower()

    safe_keywords = [
        "university", "college", "student", "class",
        "exam", "teacher", "education", "study"
    ]

    return any(word in text for word in safe_keywords)

print("=== Offline Cybersecurity Detector ===")
print("Type 'exit' to stop")

while True:
    text = input("\nEnter message/email: ")

    if text.lower() == "exit":
        break

    # 1️⃣ Safe override FIRST (important fix)
    if safe_override(text):
        print("✅ Safe (Educational Content)")
        continue

    # 2️⃣ Phishing Email Detection
    if predict(email_model, email_vec, text) == 1:
        print("⚠️ Phishing Email")

    # 3️⃣ Spam Detection
    elif predict(spam_model, spam_vec, text) == 1:
        print("❌ Spam")

    # 4️⃣ Hate Speech Detection
    elif predict(hate_model, hate_vec, text) == 1:
        print("⚠️ Hate Speech")

    # 5️⃣ Malicious URL Detection
    elif is_malicious_url(text):
        print("⚠️ Malicious Link")

    # 6️⃣ Safe
    else:
        print("✅ Safe")