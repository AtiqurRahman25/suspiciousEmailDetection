import re

def is_malicious_url(text):
    """
    Heuristic analysis to detect suspicious links.
    """
    text = text.lower().strip()

    # Improved Regex: Catches domains even without http:// or www.
    # Pattern looks for something.extension
    url_pattern = r'([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
    urls = re.findall(url_pattern, text)

    for url in urls:
        # 1. Suspicious TLD (Top Level Domain) check
        # This will catch google.xyz, login.top, etc.
        suspicious_tlds = [".xyz", ".top", ".click", ".win", ".bid", ".loan", ".date"]
        if any(url.endswith(tld) for tld in suspicious_tlds):
            return True

        # 2. Phishing Keywords in URL
        if any(word in url for word in ["login", "verify", "bank", "secure", "update", "free"]):
            return True

        # 3. Subdomain Stuffing (e.g., www.paypal.check.login.secure.com)
        if url.count('.') > 3:
            return True

        # 4. Obfuscation check
        if "@" in url:
            return True

    # 5. Malformed protocol check
    if "http:" in text and "http://" not in text:
        return True

    return False

def clean_text(text):
    """Basic text cleaning for ML models."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()