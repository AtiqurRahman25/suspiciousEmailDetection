import pickle

def load_model():
    with open("saved_model/spam_model.pkl", "rb") as f:
        model, vectorizer = pickle.load(f)
    return model, vectorizer


def predict_spam(text, model, vectorizer):
    # Convert text into numerical form
    text_vec = vectorizer.transform([text])

    # Predict (0 = not spam, 1 = spam)
    prediction = model.predict(text_vec)[0]

    return prediction