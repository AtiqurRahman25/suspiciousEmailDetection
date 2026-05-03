from model import load_spam_model, load_hate_model

spam_model, spam_vec = load_spam_model()
hate_model, hate_vec = load_hate_model()

def predict(model, vec, text):
    return model.predict(vec.transform([text]))[0]

print("=== Offline Detector ===")

while True:
    text = input("\nEnter message: ")

    if text.lower() == "exit":
        break

    # Spam check
    if predict(spam_model, spam_vec, text) == 1:
        print("❌ Spam")

    # Hate speech check
    elif predict(hate_model, hate_vec, text) == 1:
        print("⚠️ Hate Speech")

    else:
        print("✅ Safe")