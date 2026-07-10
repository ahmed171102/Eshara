# Eshara — Web Application

This is the complete, production-ready three-tier web application for the **Eshara** (إشارة) Sign Language Recognition system, as documented in **Chapter 5** of the thesis.

## Structure

```
application/
├── frontend/          # React + Vite SPA (Client Tier)
├── backend/           # Node.js + Express REST API (Application Tier)
├── model-services/    # FastAPI AI Inference Server (Inference Tier)
├── database/          # Prisma schema + migration history (standalone)
├── education_module/  # Education tab component showcase
├── docs/              # Thesis PDF and project documentation
└── Start-Eshara.bat   # One-click launcher for all three services
```

## Running the Application

Simply run from this directory:

```bash
Start-Eshara.bat
```

This opens three terminal windows and starts all services simultaneously:

| Service | URL | Technology |
|---|---|---|
| Frontend UI | http://localhost:5173 | React + Vite |
| Backend API | http://localhost:3000 | Node.js + Express + Prisma + SQLite |
| Model Services | http://localhost:8000 | FastAPI + TensorFlow + PyTorch |

## Architecture Overview

The three tiers are strictly decoupled so that AI inference does not interfere with UI responsiveness:

1. **Client Tier** — React SPA captures webcam frames as base64 JPEG and communicates over REST + Socket.IO
2. **Application Tier** — Node.js/Express authenticates JWT tokens and proxies `/predict` to FastAPI (the ML ports are never public-facing)
3. **Inference Tier** — FastAPI dispatches by `language` + `mode` to the correct inference engine

See the full thesis (Chapter 5) for the sequence diagram, ERD, class diagram, deployment diagram, and performance tables.
