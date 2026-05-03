from transformers import pipeline

# Load BERT model once
classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert"
)

def predict_hate(text):
    result = classifier(text)[0]

    label = result["label"]
    score = result["score"]

    # Handle toxic classification
    if "TOXIC" in label.upper() and score > 0.6:
        return 1
    return 0