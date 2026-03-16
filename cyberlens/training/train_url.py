from models.url_classifier import URLClassifier


if __name__ == "__main__":
    model = URLClassifier()
    print(model.predict("http://secure-login.example.com"))