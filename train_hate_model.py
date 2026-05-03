import pandas as pd
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# Load dataset
data = pd.read_csv("D:\Arvin\suspiciousEmailDetection\datasets\labeled_data.csv")

# Rename columns (Kaggle format)
data = data.rename(columns={"tweet": "text", "class": "label"})

# Keep only needed columns
data = data[['text', 'label']]

# Convert labels:
# 0 = hate, 1 = offensive, 2 = neutral
# We simplify → hate/offensive = 1, neutral = 0
data['label'] = data['label'].apply(lambda x: 1 if x != 2 else 0)

# Remove missing values
data = data.dropna()

# Split data
X = data['text']
y = data['label']

# TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english')
X_vec = vectorizer.fit_transform(X)

# Train SVM model (better for text)
model = LinearSVC(class_weight='balanced', max_iter=1000)
model.fit(X_vec, y)

# Create folder if not exists
os.makedirs("saved_model", exist_ok=True)

# Save model
with open("saved_model/hate_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ Hate speech model (SVM) trained and saved!")