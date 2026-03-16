from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from explainer import explain_scan
from risk_scorer import classify_severity, compute_risk_score


app = FastAPI(title="CyberLens API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    email_text: str = ""
    url: str = ""
    media_type: str = Field(default="audio")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/scan")
def scan(payload: ScanRequest) -> dict:
    score = compute_risk_score(payload.email_text, payload.url, payload.media_type)
    severity = classify_severity(score)
    explanation = explain_scan(payload.email_text, payload.url, score, severity)

    return {
        "score": score,
        "severity": severity,
        "explanation": explanation,
        "signals": {
            "email_length": len(payload.email_text),
            "url_present": bool(payload.url),
            "media_type": payload.media_type,
        },
    }