from model import load_model, predict_spam
from utils import contains_hate_speech

# Load model
model, vectorizer = load_model()

print("=== Offline Message Detector ===")
print("Type 'exit' to stop")

while True:
    text = input("\nEnter message: ")

    if text.lower() == "exit":
        break

    # Step 1: Spam detection (ML)
    if predict_spam(text, model, vectorizer) == 1:
        print("❌ Spam")

    # Step 2: Hate speech detection (rules)
    elif contains_hate_speech(text):
        print("⚠️ Hate Speech")

    else:
        print("✅ Safe")