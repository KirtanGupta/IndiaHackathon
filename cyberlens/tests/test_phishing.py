from backend.risk_scorer import compute_phase_scan, score_email


def test_email_keywords_raise_risk():
    result = score_email("Urgent action required. Verify your password now.")
    assert result["score"] >= 40
    assert result["severity"] in {"medium", "high"}


def test_benign_email_stays_lower_risk():
    result = score_email("Weekly update for the project meeting tomorrow.")
    assert result["score"] < 40


def test_strong_fraud_email_scores_high():
    text = """Dear Customer, We have detected unusual activity in your bank account. Your account will be temporarily suspended within the next 24 hours. To avoid suspension, please verify your account immediately by clicking the secure link below: http://secure-bank-verification-update.com/login Failure to verify your account will result in permanent account closure."""
    result = score_email(text)
    assert result["score"] >= 75
    assert result["severity"] == "high"


def test_prize_and_card_detail_bait_scores_medium_or_higher():
    result = score_email('You have won a prize verify card details now')
    assert result["label"] == "phishing"
    assert result["score"] >= 40
    assert result["severity"] in {"medium", "high"}


def test_email_phase_does_not_include_other_models():
    result = compute_phase_scan(
        "Weekly update for the project meeting tomorrow.",
        "http://secure-login.example.com/reset",
        "video",
        "email",
    )
    assert result["active_phase"] == "email"
    assert result["score"] == result["modules"]["email"]["score"]
    assert result["modules"]["url"]["source"] == "inactive"
    assert result["modules"]["deepfake"]["source"] == "inactive"