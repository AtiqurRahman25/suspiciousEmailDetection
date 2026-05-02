def contains_hate_speech(text):
    # Simple offline keyword-based detection
    hate_words = [
        "hate", "kill", "stupid", "idiot", "ugly", "trash", "racist"
    ]

    text = text.lower()

    for word in hate_words:
        if word in text:
            return True

    return False