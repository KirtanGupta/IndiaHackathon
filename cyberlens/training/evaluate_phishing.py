from __future__ import annotations

import csv
from pathlib import Path

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from train_phishing import PROJECT_ROOT, build_pipeline, load_training_rows

REALISTIC_EVAL_PATH = PROJECT_ROOT / "data" / "phishing_realistic_eval.csv"


def _probability_map(classes: list[str], probs: list[float]) -> dict[str, float]:
    return {classes[index]: round(float(probs[index]), 4) for index in range(len(classes))}


def load_realistic_eval_rows() -> tuple[list[str], list[str]]:
    texts: list[str] = []
    labels: list[str] = []

    with REALISTIC_EVAL_PATH.open("r", encoding="utf-8", newline="") as csv_file:
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

    return texts, labels


def evaluate() -> dict:
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
    probabilities = pipeline.predict_proba(test_texts)
    classes = [str(label) for label in pipeline.classes_]
    report = classification_report(test_labels, predictions, output_dict=True)
    matrix = confusion_matrix(test_labels, predictions, labels=classes)
    accuracy = float(accuracy_score(test_labels, predictions))

    mistakes: list[dict[str, object]] = []
    for text, actual, predicted, probs in zip(test_texts, test_labels, predictions, probabilities):
        if actual != predicted:
            mistakes.append(
                {
                    "actual": actual,
                    "predicted": predicted,
                    "probabilities": _probability_map(classes, probs),
                    "text": text[:180],
                }
            )

    realistic_texts, realistic_labels = load_realistic_eval_rows()
    realistic_predictions = pipeline.predict(realistic_texts)
    realistic_probabilities = pipeline.predict_proba(realistic_texts)
    realistic_report = classification_report(realistic_labels, realistic_predictions, output_dict=True)
    realistic_matrix = confusion_matrix(realistic_labels, realistic_predictions, labels=classes)
    realistic_accuracy = float(accuracy_score(realistic_labels, realistic_predictions))

    realistic_errors: list[dict[str, object]] = []
    for text, actual, predicted, probs in zip(
        realistic_texts,
        realistic_labels,
        realistic_predictions,
        realistic_probabilities,
    ):
        if actual != predicted:
            realistic_errors.append(
                {
                    "actual": actual,
                    "predicted": predicted,
                    "probabilities": _probability_map(classes, probs),
                    "text": text[:180],
                }
            )

    sample_inputs = [
        "We detected unusual activity and need you to confirm your identity immediately",
        "provide your id and password for reward",
        "Weekly project update and meeting notes for tomorrow",
        "Trip receipt attached for your records and expense filing",
        "You have won a prize verify card details now",
    ]
    sample_predictions: list[dict[str, object]] = []
    for text in sample_inputs:
        probs = pipeline.predict_proba([text])[0]
        sample_predictions.append(
            {
                "text": text,
                "predicted": pipeline.predict([text])[0],
                "probabilities": _probability_map(classes, probs),
            }
        )

    return {
        "samples": len(texts),
        "train_samples": len(train_texts),
        "test_samples": len(test_texts),
        "accuracy": round(accuracy, 4),
        "labels": classes,
        "classification_report": report,
        "confusion_matrix": matrix.tolist(),
        "mistakes": mistakes[:5],
        "realistic_eval": {
            "path": str(REALISTIC_EVAL_PATH),
            "samples": len(realistic_texts),
            "accuracy": round(realistic_accuracy, 4),
            "classification_report": realistic_report,
            "confusion_matrix": realistic_matrix.tolist(),
            "mistakes": realistic_errors[:10],
        },
        "sample_predictions": sample_predictions,
    }


if __name__ == "__main__":
    result = evaluate()
    print(f"Dataset size: {result['samples']}")
    print(f"Train/Test split: {result['train_samples']}/{result['test_samples']}")
    print(f"Synthetic holdout accuracy: {result['accuracy']}")
    print("Synthetic holdout confusion matrix rows=actual cols=predicted")
    print(f"Labels: {', '.join(result['labels'])}")
    for row in result['confusion_matrix']:
        print(row)
    print("Synthetic classification report")
    for label in result['labels']:
        metrics = result['classification_report'][label]
        print(
            f"{label}: precision={metrics['precision']:.4f} recall={metrics['recall']:.4f} "
            f"f1={metrics['f1-score']:.4f} support={int(metrics['support'])}"
        )
    realistic = result['realistic_eval']
    print(f"Realistic eval file: {realistic['path']}")
    print(f"Realistic eval samples: {realistic['samples']}")
    print(f"Realistic eval accuracy: {realistic['accuracy']}")
    print("Realistic eval confusion matrix rows=actual cols=predicted")
    for row in realistic['confusion_matrix']:
        print(row)
    print("Realistic classification report")
    for label in result['labels']:
        metrics = realistic['classification_report'][label]
        print(
            f"{label}: precision={metrics['precision']:.4f} recall={metrics['recall']:.4f} "
            f"f1={metrics['f1-score']:.4f} support={int(metrics['support'])}"
        )
    print("Sample predictions")
    for item in result['sample_predictions']:
        print(f"- {item['predicted']}: {item['text']}")
        print(f"  probs={item['probabilities']}")
    if realistic['mistakes']:
        print("Realistic eval mistakes")
        for item in realistic['mistakes']:
            print(f"- actual={item['actual']} predicted={item['predicted']} probs={item['probabilities']}")
            print(f"  text={item['text']}")
    else:
        print("Realistic eval mistakes: none")
    if result['mistakes']:
        print("Synthetic holdout mistakes")
        for item in result['mistakes']:
            print(f"- actual={item['actual']} predicted={item['predicted']} probs={item['probabilities']}")
            print(f"  text={item['text']}")
    else:
        print("Synthetic holdout mistakes: none")
