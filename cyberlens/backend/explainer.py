def explain_scan(email_text: str, url: str, score: int, severity: str) -> str:
    reasons = []

    if any(token in email_text.lower() for token in ["urgent", "verify", "password"]):
        reasons.append("email language suggests pressure or credential harvesting")
    if url:
        reasons.append("a link is present and should be validated before clicking")
    if url.startswith("http://"):
        reasons.append("the URL uses insecure HTTP instead of HTTPS")
    if not reasons:
        reasons.append("few suspicious indicators were detected in this scan")

    joined = "; ".join(reasons)
    return f"Risk score {score}/100 ({severity}). {joined}."