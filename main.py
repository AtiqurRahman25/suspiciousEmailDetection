from model import load_model, predict_spam

# Load trained model once
model, vectorizer = load_model()

print("=== Offline Spam Detector ===")
print("Type 'exit' to stop")

while True:
    text = input("\nEnter message: ")

    if text.lower() == "exit":
        break

    result = predict_spam(text, model, vectorizer)

    if result == 1:
        print("❌ Spam")
    else:
        print("✅ Not Spam")