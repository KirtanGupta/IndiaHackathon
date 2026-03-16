# CyberLens

CyberLens is a starter full-stack cybersecurity demo that estimates risk from email text, URLs, and media indicators.

## Structure

- `backend/`: FastAPI service with a demo `/scan` endpoint
- `frontend/`: Vite app config and deployment scripts
- `src/`: React app entrypoint and page layout
- `components/`: Reusable visual components
- `api/`: Frontend API helper
- `models/`: Placeholder model wrappers
- `training/`: Starter training scripts
- `tests/`: Backend smoke tests

## Run Backend

```bash
cd cyberlens/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Run Frontend

```bash
cd cyberlens/frontend
npm install
npm run dev
```

The frontend defaults to `http://localhost:8000` for API calls.