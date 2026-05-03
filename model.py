import pickle

# Load spam model
def load_spam_model():
    with open("saved_model/spam_model.pkl", "rb") as f:
        model, vectorizer = pickle.load(f)
    return model, vectorizer

# Load hate speech model
def load_hate_model():
    with open("saved_model/hate_model.pkl", "rb") as f:
        model, vectorizer = pickle.load(f)
    return model, vectorizer