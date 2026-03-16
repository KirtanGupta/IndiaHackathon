from backend.risk_scorer import classify_severity, compute_risk_score


def test_phishing_keywords_raise_score():
    score = compute_risk_score("Urgent verify your password now", "", "audio")
    assert score >= 40
    assert classify_severity(score) in {"medium", "high"}