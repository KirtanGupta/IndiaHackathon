from pathlib import Path
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.phishing_classifier import PhishingClassifier

EMAIL_TOKENS = {
    "urgent": 18,
    "verify": 14,
    "password": 18,
    "bank": 10,
    "suspended": 12,
    "security": 8,
    "account": 6,
    "login": 12,
    "credentials": 16,
    "prize": 14,
    "reward": 12,
    "card": 12,
    "details": 8,
}

EMAIL_PATTERNS = {
    "within 24 hours": 14,
    "click the secure link": 18,
    "click the link below": 18,
    "account closure": 20,
    "temporarily suspended": 16,
    "unusual activity": 14,
    "verify your account": 18,
    "confirm your identity": 18,
    "customer security department": 16,
    "avoid suspension": 16,
    "permanent account closure": 22,
    "won a prize": 24,
    "verify card details": 24,
    "claim your reward": 20,
}

URL_TOKENS = {
    "login": 16,
    "secure": 10,
    "verify": 10,
    "free": 8,
    "gift": 8,
    "@": 18,
}

PHISHING_MODEL = PhishingClassifier()
PHASE_ORDER = ["email", "url", "deepfake"]
URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)


def classify_severity(score: int) -> str:
    if score >= 75:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _heuristic_email_signals(email_text: str) -> tuple[list[str], int]:
    lowered = email_text.lower()
    matched: list[str] = []
    score = 0

    for token, weight in EMAIL_TOKENS.items():
        if token in lowered:
            matched.append(token)
            score += weight

    for pattern, weight in EMAIL_PATTERNS.items():
        if pattern in lowered:
            matched.append(pattern)
            score += weight

    found_urls = URL_PATTERN.findall(email_text)
    for url in found_urls:
        matched.append("embedded-link")
        score += 18
        lowered_url = url.lower()
        if url.startswith("http://"):
            matched.append("embedded-http-link")
            score += 14
        if any(token in lowered_url for token in ["login", "verify", "secure", "update"]):
            matched.append("suspicious-link-terms")
            score += 16

    if len(matched) >= 5:
        matched.append("multi-signal-phishing-pattern")
        score += 12

    return list(dict.fromkeys(matched)), min(score, 100)


def score_email(email_text: str) -> dict:
    matched, heuristic_score = _heuristic_email_signals(email_text)

    if PHISHING_MODEL.is_available():
        prediction = PHISHING_MODEL.predict(email_text)
        phishing_probability = prediction["probabilities"].get("phishing", 0.0)
        model_component = round(phishing_probability * 100 * 0.4)
        heuristic_component = round(heuristic_score * 0.6)
        score = min(model_component + heuristic_component, 100)
        summary = f"ML phishing classifier predicted {prediction['label']}"
        return {
            "module": "email",
            "score": score,
            "severity": classify_severity(score),
            "matched_signals": matched or [f"model:{prediction['label']}"] ,
            "summary": summary,
            "label": prediction["label"],
            "confidence": prediction["confidence"],
            "probabilities": prediction["probabilities"],
            "score_breakdown": {
                "model_component": model_component,
                "heuristic_component": heuristic_component,
                "raw_heuristic_score": heuristic_score,
            },
            "source": "model",
        }

    return {
        "module": "email",
        "score": heuristic_score,
        "severity": classify_severity(heuristic_score),
        "matched_signals": matched,
        "summary": "Phishing language scan",
        "label": "phishing" if heuristic_score >= 40 else "benign",
        "confidence": round(heuristic_score / 100, 4),
        "score_breakdown": {
            "model_component": 0,
            "heuristic_component": heuristic_score,
            "raw_heuristic_score": heuristic_score,
        },
        "source": "heuristic",
    }


def score_url(url: str) -> dict:
    lowered = url.lower()
    matched = [token for token in URL_TOKENS if token in lowered]
    score = sum(URL_TOKENS[token] for token in matched)

    if url.startswith("http://"):
        matched.append("http")
        score += 14
    if len(url) > 60:
        matched.append("long-url")
        score += 8

    score = min(100, score)
    return {
        "module": "url",
        "score": score,
        "severity": classify_severity(score),
        "matched_signals": matched,
        "summary": "Malicious URL heuristics",
        "source": "heuristic",
    }


def score_deepfake(media_type: str) -> dict:
    score = 28 if media_type.lower() == "audio" else 44
    matched = [f"media:{media_type.lower()}"]

    if media_type.lower() == "video":
        matched.append("frame-consistency-review")
    else:
        matched.append("voice-authenticity-review")

    return {
        "module": "deepfake",
        "score": score,
        "severity": classify_severity(score),
        "matched_signals": matched,
        "summary": "Media authenticity pre-check",
        "source": "heuristic",
    }


def _empty_module_result(module: str) -> dict:
    return {
        "module": module,
        "score": 0,
        "severity": "low",
        "matched_signals": [],
        "summary": f"{module.title()} phase not run in this scan",
        "source": "inactive",
    }


def compute_phase_scan(email_text: str, url: str, media_type: str, active_phase: str) -> dict:
    active_phase = active_phase if active_phase in PHASE_ORDER else "email"

    active_result = {
        "email": score_email(email_text),
        "url": score_url(url),
        "deepfake": score_deepfake(media_type),
    }[active_phase]

    modules = {phase: _empty_module_result(phase) for phase in PHASE_ORDER}
    modules[active_phase] = active_result
    ordered_modules = [modules[phase] for phase in PHASE_ORDER]

    return {
        "active_phase": active_phase,
        "phase_order": PHASE_ORDER,
        "modules": modules,
        "ordered_modules": ordered_modules,
        "score": active_result["score"],
        "severity": active_result["severity"],
    }