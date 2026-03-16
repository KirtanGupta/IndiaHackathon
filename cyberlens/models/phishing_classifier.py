class PhishingClassifier:
    def predict(self, text: str) -> dict:
        suspicious = any(token in text.lower() for token in ["verify", "urgent", "password"])
        return {
            "label": "phishing" if suspicious else "safe",
            "confidence": 0.82 if suspicious else 0.22,
        }