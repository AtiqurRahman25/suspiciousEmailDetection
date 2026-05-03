import pandas as pd
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# Load dataset (CEAS_08.csv)
data = pd.read_csv("D:\Arvin\suspiciousEmailDetection\datasets\CEAS_08.csv")

# Try to detect columns safely
print(data.columns)

# Adjust these if needed after printing columns:
TEXT_COLUMN = "body"
LABEL_COLUMN = "label"

# Keep only needed columns
data = data[[TEXT_COLUMN, LABEL_COLUMN]].dropna()

X = data[TEXT_COLUMN]
y = data[LABEL_COLUMN]

# TF-IDF conversion
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_vec = vectorizer.fit_transform(X)

# Model (good for text classification)
model = LinearSVC(class_weight='balanced')
model.fit(X_vec, y)

# Save model
os.makedirs("saved_model", exist_ok=True)

with open("saved_model/email_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ Phishing email model trained successfully!")