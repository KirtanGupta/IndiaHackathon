class URLClassifier:
    def predict(self, url: str) -> dict:
        suspicious = any(token in url.lower() for token in ["login", "secure", "@"])
        return {
            "label": "malicious" if suspicious else "benign",
            "confidence": 0.79 if suspicious else 0.18,
        }