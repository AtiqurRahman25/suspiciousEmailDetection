import re

def is_malicious_url(text):
    text = text.lower()

    # Find URLs
    url_pattern = r'(https?://\S+|www\.\S+)'
    urls = re.findall(url_pattern, text)

    for url in urls:
        # suspicious keywords
        if any(word in url for word in ["login", "verify", "free", "click", "bank"]):
            return True

        # too many dots (fake domains)
        if url.count('.') > 3:
            return True

        # suspicious character
        if "@" in url:
            return True

    # broken URL pattern like http:abc.xyz
    if "http:" in text and "http://" not in text:
        return True

    return False