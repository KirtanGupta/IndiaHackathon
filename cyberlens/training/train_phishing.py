from models.phishing_classifier import PhishingClassifier


if __name__ == "__main__":
    model = PhishingClassifier()
    print(model.predict("Urgent: verify your password now"))