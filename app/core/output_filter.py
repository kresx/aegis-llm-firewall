import re

PII_PATTERNS = {
    "api_key": r"sk-[a-zA-Z0-9]{32,}",
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b"
}

def filter_output(ai_response: str) -> str:
    """Scans AI response for sensitive data leakage."""
    filtered_text = ai_response
    for label, pattern in PII_PATTERNS.items():
        if re.search(pattern, ai_response):
            filtered_text = re.sub(pattern, f"[REDACTED_{label.upper()}]", filtered_text)
    return filtered_text