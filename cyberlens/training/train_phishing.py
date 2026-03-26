from __future__ import annotations

import csv
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "sample_emails.csv"
MODEL_PATH = PROJECT_ROOT / "saved_models" / "phishing_model.pkl"


def load_training_rows() -> tuple[list[str], list[str]]:
    texts: list[str] = []
    labels: list[str] = []

    with DATA_PATH.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            text = " ".join(
                [
                    row["sender"].strip(),
                    row["subject"].strip(),
                    row["body"].strip(),
                ]
            )
            texts.append(text)
            labels.append(row["label"].strip())

    if len(set(labels)) < 2:
        raise ValueError("Need at least two classes to train the phishing model")

    return texts, labels


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "vectorizer",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    stop_words="english",
                    min_df=1,
                ),
            ),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )


def train() -> dict:
    texts, labels = load_training_rows()
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    pipeline = build_pipeline()
    pipeline.fit(train_texts, train_labels)

    predictions = pipeline.predict(test_texts)
    report = classification_report(test_labels, predictions, output_dict=False)
    accuracy = accuracy_score(test_labels, predictions)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": pipeline, "labels": list(pipeline.classes_)}, MODEL_PATH)

    return {
        "samples": len(texts),
        "train_samples": len(train_texts),
        "test_samples": len(test_texts),
        "labels": sorted(set(labels)),
        "accuracy": round(float(accuracy), 4),
        "model_path": str(MODEL_PATH),
        "report": report,
    }


if __name__ == "__main__":
    result = train()
    print(f"Trained phishing model on {result['samples']} samples")
    print(f"Train/Test split: {result['train_samples']}/{result['test_samples']}")
    print(f"Labels: {', '.join(result['labels'])}")
    print(f"Accuracy: {result['accuracy']}")
    print(f"Saved to: {result['model_path']}")
    print(result["report"])
