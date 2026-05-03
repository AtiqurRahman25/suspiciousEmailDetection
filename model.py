import pickle

# Spam model
def load_spam_model():
    with open("saved_model/spam_model.pkl", "rb") as f:
        model, vectorizer = pickle.load(f)
    return model, vectorizer

# Hate speech model
def load_hate_model():
    with open("saved_model/hate_model.pkl", "rb") as f:
        model, vectorizer = pickle.load(f)
    return model, vectorizer

# Email phishing model (IMPORTANT - missing earlier)
def load_email_model():
    with open("saved_model/email_model.pkl", "rb") as f:
        model, vectorizer = pickle.load(f)
    return model, vectorizer