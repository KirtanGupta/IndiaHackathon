from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from explainer import explain_scan
from risk_scorer import compute_phase_scan


app = FastAPI(title="CyberLens API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    active_phase: str = Field(default="email")
    email_text: str = ""
    url: str = ""
    media_type: str = Field(default="audio")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "project": "CyberLens"}


@app.get("/roadmap")
def roadmap() -> dict:
    return {
        "phases": [
            "foundation",
            "api",
            "training",
            "explainability",
            "frontend-demo",
            "testing",
            "deployment",
        ],
        "demo_order": ["email", "url", "deepfake"],
    }


@app.post("/scan")
def scan(payload: ScanRequest) -> dict:
    result = compute_phase_scan(payload.email_text, payload.url, payload.media_type, payload.active_phase)
    explanation = explain_scan(result)

    return {
        **result,
        "explanation": explanation["overall"],
        "module_explanations": explanation["modules"],
        "signals": {
            "email_length": len(payload.email_text),
            "url_present": bool(payload.url),
            "media_type": payload.media_type,
        },
    }