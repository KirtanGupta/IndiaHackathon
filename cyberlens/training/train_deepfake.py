from models.deepfake_detector import DeepfakeDetector


if __name__ == "__main__":
    model = DeepfakeDetector()
    print(model.predict("sample.mp4"))