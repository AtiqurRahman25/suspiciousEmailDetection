import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv(r"D:\Arvin\suspiciousEmailDetection\datasets\CEAS_08.csv")

TEXT_COLUMN = "body"
LABEL_COLUMN = "label"

# Clean data
data = data[[TEXT_COLUMN, LABEL_COLUMN]].dropna()
X = data[TEXT_COLUMN]
y = data[LABEL_COLUMN]

# TF-IDF conversion
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1,2)) # Added n-grams
X_vec = vectorizer.fit_transform(X)

# Using Random Forest to get probability scores
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_vec, y)

# Save model
os.makedirs("saved_model", exist_ok=True)
with open("saved_model/email_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ Enhanced Phishing model trained with Probability support!")