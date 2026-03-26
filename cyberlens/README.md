# CyberLens

CyberLens is a phased full-stack cybersecurity demo for hackathon judging. The implementation and demo order intentionally match the product flow:

1. Email phishing detection
2. Suspicious URL detection
3. Deepfake media detection

## Why The Structure Matters

Each layer depends on the previous one. The backend must exist before model inference can be wired in, explainability must exist before the frontend can visualize it, and deployment only happens after the local flow is stable.

See [BUILD_PLAN.md](./BUILD_PLAN.md) for the working order.

## Current Structure

- `backend/`: FastAPI API and risk orchestration
- `frontend/`: Vite config for local and hosted builds
- `src/`: React app shell and phase-driven page flow
- `components/`: UI blocks for inputs, results, and logs
- `api/`: Frontend API requests
- `models/`: Placeholder model wrappers until trained artifacts are integrated
- `training/`: Training script entry points
- `tests/`: Smoke tests for scoring logic and model wrappers

## Local Run

### Backend

```bash
cd cyberlens/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd cyberlens/frontend
npm install
npm run dev
```

The frontend expects `VITE_API_BASE_URL=http://localhost:8000`.

## Phishing Model

```bash
python cyberlens/training/generate_phishing_dataset.py
python cyberlens/training/train_phishing.py
python cyberlens/training/evaluate_phishing.py
```

The evaluation script prints held-out accuracy, confusion matrix, class metrics, and a few example predictions.
