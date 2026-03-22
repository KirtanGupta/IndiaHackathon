from backend.risk_scorer import compute_phase_scan, score_url


def test_http_and_login_tokens_raise_url_risk():
    result = score_url("http://secure-login.example.com")
    assert result["score"] > 20
    assert "http" in result["matched_signals"]


def test_safe_url_stays_lower_risk():
    result = score_url("https://docs.python.org/3/tutorial/")
    assert result["score"] < 20


def test_url_phase_does_not_include_other_models():
    result = compute_phase_scan(
        "Urgent verify your password now.",
        "https://docs.python.org/3/tutorial/",
        "video",
        "url",
    )
    assert result["active_phase"] == "url"
    assert result["score"] == result["modules"]["url"]["score"]
    assert result["modules"]["email"]["source"] == "inactive"
    assert result["modules"]["deepfake"]["source"] == "inactive"