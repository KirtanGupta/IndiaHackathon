from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib


MODEL_PATH = Path(__file__).resolve().parents[1] / "saved_models" / "phishing_model.pkl"


class PhishingClassifier:
    def __init__(self, model_path: Path | None = None) -> None:
        self.model_path = model_path or MODEL_PATH
        self._bundle: dict[str, Any] | None = None

    def is_available(self) -> bool:
        return self.model_path.exists()

    def _load_bundle(self) -> dict[str, Any]:
        if self._bundle is None:
            if not self.model_path.exists():
                raise FileNotFoundError(f"Missing phishing model: {self.model_path}")
            self._bundle = joblib.load(self.model_path)
        return self._bundle

    def predict(self, text: str) -> dict:
        bundle = self._load_bundle()
        model = bundle["model"]
        labels = [str(label) for label in bundle["labels"]]

        probabilities = model.predict_proba([text])[0]
        probability_map = {
            labels[index]: float(probabilities[index])
            for index in range(len(labels))
        }
        label = max(probability_map, key=probability_map.get)
        confidence = probability_map[label]

        return {
            "label": label,
            "confidence": round(confidence, 4),
            "probabilities": {key: round(value, 4) for key, value in probability_map.items()},
        }