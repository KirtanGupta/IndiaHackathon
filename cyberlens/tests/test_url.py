from backend.risk_scorer import compute_risk_score


def test_http_url_increases_risk():
    safe_score = compute_risk_score("hello", "https://example.com", "audio")
    risky_score = compute_risk_score("hello", "http://secure-login.example.com", "audio")
    assert risky_score > safe_score