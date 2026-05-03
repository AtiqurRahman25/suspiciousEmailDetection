import re

def is_malicious_url(text):
    text = text.lower()

    url_pattern = r'(https?://\S+|www\.\S+)'
    urls = re.findall(url_pattern, text)

    for url in urls:
        if any(word in url for word in ["login", "verify", "free", "click", "bank"]):
            return True
        if url.count('.') > 3:
            return True
        if "@" in url:
            return True

    if "http:" in text and "http://" not in text:
        return True

    return False