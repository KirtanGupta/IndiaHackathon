class DeepfakeDetector:
    def predict(self, media_path: str) -> dict:
        suspicious = media_path.lower().endswith(".mp4")
        return {
            "label": "suspected-deepfake" if suspicious else "likely-authentic",
            "confidence": 0.71 if suspicious else 0.31,
        }