import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier # Change from LinearSVC

# Load dataset
data = pd.read_csv(r"D:\Arvin\suspiciousEmailDetection\datasets\labeled_data.csv")

# Rename columns
data = data.rename(columns={"tweet": "text", "class": "label"})
data = data[['text', 'label']].dropna()

# Labeling logic: 0=hate, 1=offensive, 2=neutral
# We keep them separate or use your 1/0 logic, but Random Forest handles it better
data['label'] = data['label'].apply(lambda x: 1 if x != 2 else 0)

X = data['text']
y = data['label']

# TF-IDF with Bi-grams (Crucial for catching "killed the person")
# ngram_range=(1,2) helps the model see word pairs
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=10000)
X_vec = vectorizer.fit_transform(X)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_vec, y)

# Save
os.makedirs("saved_model", exist_ok=True)
with open("saved_model/hate_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ Hate/Threat model (Random Forest) trained with probability support!")