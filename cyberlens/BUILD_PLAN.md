# CyberLens Build Plan

This project is intentionally built in phases. Do not advance a phase until the current one works locally.

## Phase 1: Foundation

- FastAPI backend boots locally
- React frontend boots locally
- Frontend can call backend health and scan endpoints
- Repo structure is stable

## Phase 2: API Layer

- `/scan` accepts email, URL, and media input
- API returns ordered module results: email -> url -> deepfake
- Risk score and explanation are deterministic and demo-safe

## Phase 3: Model Training

- Train phishing classifier
- Train malicious URL classifier
- Train deepfake detector
- Save artifacts in `saved_models/`

## Phase 4: Explainability

- Add feature contribution output
- Wire SHAP or proxy explanation values into backend
- Expose explanation payloads to frontend charts

## Phase 5: Frontend Demo Flow

- Email step first
- URL step second
- Deepfake step third
- Incident log and risk summary update after each scan

## Phase 6: Testing

- Backend tests pass locally
- Frontend build succeeds locally
- End-to-end demo flow is manually validated

## Phase 7: Deployment

- Backend deployed after local verification
- Frontend deployed after backend URL is stable
- Demo script follows email -> url -> deepfake order

## Critical Rule

A smaller system that works is better than a larger system that crashes during judging.