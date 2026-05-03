from flask import Flask, render_template, request

from model import load_spam_model, load_email_model
from utils import is_malicious_url
from db import init_db, save_message
from bert_model import predict_hate

app = Flask(__name__)

# Initialize DB
init_db()

# Load traditional ML models
spam_model, spam_vec = load_spam_model()
email_model, email_vec = load_email_model()

def predict(model, vec, text):
    return model.predict(vec.transform([text]))[0]

# Detect email-like content
def looks_like_email(text):
    text = text.lower()
    keywords = ["http", "www", "@", "verify", "account", "login", "click"]
    return any(word in text for word in keywords)

# Hard rule-based violent detection
def is_violent(text):
    text = text.lower()
    keywords = [
        "kill", "murder", "die", "hurt", "attack",
        "beat", "shoot", "destroy", "cut"
    ]
    return any(word in text for word in keywords)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    text = ""
    masked = ""

    if request.method == "POST":
        text = request.form["message"]

        # 1. Hard rule (highest priority)
        if is_violent(text):
            result = "Hate / Violent Speech"

        # 2. BERT-based hate detection
        elif predict_hate(text) == 1:
            result = "Hate Speech"

        # 3. Phishing (only email-like)
        elif looks_like_email(text) and predict(email_model, email_vec, text) == 1:
            result = "Phishing Email"

        # 4. Spam
        elif predict(spam_model, spam_vec, text) == 1:
            result = "Spam"

        # 5. Malicious URL
        elif is_malicious_url(text):
            result = "Malicious Link"

        # 6. Safe
        else:
            result = "Safe"

        # Mask unsafe content
        if result != "Safe":
            masked = "*" * len(text)

        # Save to database
        save_message(text, result)

    return render_template("index.html", result=result, text=text, masked=masked)

if __name__ == "__main__":
    app.run(debug=True)