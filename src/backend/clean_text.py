import re

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove URLs, handles (@), and special characters common in social media posts
    text = re.sub(r"http\S+|@\S+|#\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.strip()