import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# --- CONFIGURATION ---
DATASETS = {
    "email": {
        "path": r"D:\Arvin\suspiciousEmailDetection\datasets\CEAS_08.csv",
        "text_col": "body",
        "label_col": "label",
        "save_name": "email_model.pkl"
    },
    "hate": {
        "path": r"D:\Arvin\suspiciousEmailDetection\datasets\labeled_data.csv",
        "text_col": "tweet",
        "label_col": "class",
        "save_name": "hate_model.pkl"
    }
}

os.makedirs("saved_model", exist_ok=True)

def train_and_save(domain, config):
    print(f"--- Training {domain.upper()} Model ---")
    
    # Load Data
    data = pd.read_csv(config["path"])
    
    # Preprocessing for Hate dataset (mapping labels to binary)
    if domain == "hate":
        # class: 0=hate, 1=offensive, 2=neutral -> map 0,1 to 1 (threat), 2 to 0 (safe)
        data[config["label_col"]] = data[config["label_col"]].apply(lambda x: 1 if x != 2 else 0)
    
    data = data[[config["text_col"], config["label_col"]]].dropna()
    X = data[config["text_col"]]
    y = data[config["label_col"]]

    # Feature Extraction (n-grams help context like "my house" vs "the house")
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10000, ngram_range=(1,2))
    X_vec = vectorizer.fit_transform(X)

    # Random Forest allows for .predict_proba() used in your main.py
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X_vec, y)

    # Save
    save_path = os.path.join("saved_model", config["save_name"])
    with open(save_path, "wb") as f:
        pickle.dump((model, vectorizer), f)
    
    print(f"✅ {domain.capitalize()} model saved to {save_path}\n")

# Execute Training
for domain, config in DATASETS.items():
    try:
        train_and_save(domain, config)
    except Exception as e:
        print(f"❌ Error training {domain}: {e}")

print("🏁 All models are ready for the Forensic Monitor.")