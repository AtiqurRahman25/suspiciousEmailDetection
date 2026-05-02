import pandas as pd
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset (Kaggle Format B: v1, v2)
data = pd.read_csv("data/spam.csv", encoding="latin-1")

# Rename columns properly
data = data.rename(columns={'v1': 'label', 'v2': 'message'})

# Keep only needed columns
data = data[['label', 'message']]

# Convert labels: ham = 0, spam = 1
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# Remove missing values
data = data.dropna()

# Split data
X = data['message']
y = data['label']

# Convert text to numbers (TF-IDF)
vectorizer = TfidfVectorizer(stop_words='english')
X_vec = vectorizer.fit_transform(X)

# Train model (lightweight + good accuracy)
model = LogisticRegression(max_iter=1000)
model.fit(X_vec, y)

# Create folder if not exists
os.makedirs("saved_model", exist_ok=True)

# Save model + vectorizer
with open("saved_model/spam_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ Model trained and saved successfully!")