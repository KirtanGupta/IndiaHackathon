SUSPICIOUS_EMAIL_TOKENS = ["urgent", "password", "verify", "bank", "suspended"]
SUSPICIOUS_URL_TOKENS = ["login", "secure", "verify", "free", "gift"]


def compute_risk_score(email_text: str, url: str, media_type: str) -> int:
    score = 10

    lowered_email = email_text.lower()
    lowered_url = url.lower()

    score += sum(10 for token in SUSPICIOUS_EMAIL_TOKENS if token in lowered_email)
    score += sum(8 for token in SUSPICIOUS_URL_TOKENS if token in lowered_url)

    if url.startswith("http://"):
        score += 12
    if "@" in url or len(url) > 60:
        score += 10
    if media_type.lower() == "video":
        score += 6

    return min(score, 100)


def classify_severity(score: int) -> str:
    if score >= 75:
        return "high"
    if score >= 40:
        return "medium"
    return "low"