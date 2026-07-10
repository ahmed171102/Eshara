# إشارة — Eshara: Bilingual Sign Language Recognition System

> **A Graduation Project by — Arab Academy for Science, Technology and Maritime Transport (AASTMT)**  
> College of Engineering and Technology | Computer Engineering Department  
> **B.Sc. Final Year Project — July 2026**

---

## 👥 Team

| Name |
|---|
| Ahmed Adel Sayed Gouda Ahmed |
| Hadeel Gamal Eldin Mohamed Ibrahim |
| Alaa Osama Mohammed Shehab |
| Salah Mohamed Salah Ibrahim |

**Supervised by:**
- Dr. Nada Mostafa Abdelaziem Mostafa
- Dr. Reham Taher Abdelmajeed Salem Al Magraby

---

## 📖 Abstract

**Eshara** (إشارة — Arabic for "sign") is a real-time bilingual web application for **American Sign Language (ASL)** and **Arabic Sign Language (ArSL)** that supports both static letter finger-spelling and isolated-word recognition from a standard webcam.

The system follows a three-tier architecture: a **React** frontend, a **Node.js/Express** application layer for authentication and routing, and a **FastAPI** model-services layer for inference. Four standalone deep-learning models are trained with entirely separate vocabularies:

1. An ASL letter **MLP** over **78-D** engineered hand landmarks (28 deployed classes)
2. An ArSL letter **MLP** over **63-D** raw hand landmarks (32 classes)
3. An ASL word **Inception I3D** model over **32-frame 224×224** RGB clips (100 WLASL glosses)
4. An ArSL word stacked **BiLSTM** over **225-D** normalised Holistic sequences (48 frames, 100 KArSL classes)

The platform additionally features an **Education Module** built on a bilingual motion-capture pipeline, using server-side animation stitching and Dynamic Time Warping to verify sign vocabulary for pedagogical practice.

---

## 🏗️ Repository Structure

```
Eshara_GitHub_Release/
│
├── 📁 application/              The complete 3-tier web application
│   ├── frontend/                React + Vite SPA (User Interface)
│   ├── backend/                 Node.js + Express REST API + Prisma + SQLite
│   ├── model-services/          FastAPI AI Inference Server (hosts all 4 models)
│   ├── education_module/        Education tab source — Canvas2D/pose-viewer components
│   ├── docs/                    Thesis PDF and project documentation
│   └── Start-Eshara.bat         One-click launcher for all three services
│
└── 📁 4_Final_Models/           Standalone AI training artifacts
    ├── Letters Final/
    │   ├── ASL Letters Final/   English letter model (99.06% Top-1)
    │   └── ArSL Letters Final/  Arabic letter model (99.63% Top-1)
    └── Words Final/
        ├── ASL Words Final/     English word model (WLASL-100, I3D)
        └── ArSL Words Final/    Arabic word model — Issam BiLSTM bundle (99.62% Top-1)
```

---

## 🤖 The Four AI Models

| # | Model | Language | Architecture | Input Features | Classes | Accuracy |
|---|---|---|---|---|---|---|
| 1 | **ASL Letter MLP** | English | 3-hidden-layer MLP | 78-D engineered MediaPipe hand landmarks | **28** (A–Z + space + del) | **99.06%** Top-1 / 98.74% macro-F1 |
| 2 | **ArSL Letter MLP** | Arabic | MLP (512→256→64) | 63-D raw MediaPipe hand landmarks | **32** | **99.63%** Top-1 / 99.44% macro-F1 |
| 3 | **ASL Word I3D** | English | Inception I3D (PyTorch) | 32-frame × 224×224 RGB clips | **100** WLASL glosses | **65.89%** Top-1 / 84.11% Top-5 (Li et al. benchmark) |
| 4 | **ArSL Word BiLSTM** | Arabic | Stacked Bidirectional LSTM | 225-D nose/wrist-normalised Holistic (48 frames) | **100** KArSL classes | **99.62%** Top-1 |

> ASL and ArSL have entirely separate vocabularies and feature spaces — four specialised pipelines are used rather than a single shared multilingual model.

---

## 🚀 Quick Start

### Prerequisites
- Node.js v18+
- Python 3.10+
- A standard webcam

### 1. Install Dependencies

```bash
# Backend (Node.js)
cd application/backend
npm install

# Frontend (React)
cd application/frontend
npm install

# Model Services (Python/FastAPI)
cd application/model-services
pip install -r requirements.txt
```

### 2. Launch Everything

From the `application/` directory, simply double-click or run:

```bash
Start-Eshara.bat
```

This opens **three separate terminal windows** and launches all services at once:

| Service | URL | Technology |
|---|---|---|
| Frontend UI | http://localhost:5173 | React + Vite |
| Backend API | http://localhost:3000 | Node.js + Express + Prisma |
| Model Services | http://localhost:8000 | FastAPI + TensorFlow + PyTorch |

---

## 🏛️ System Architecture

Eshara adopts a **decoupled, three-tier architecture** so that AI inference does not interfere with UI responsiveness:

```
┌─────────────────────────────────────────────────────┐
│  CLIENT TIER (React + Vite)                         │
│  - Webcam capture (base64 JPEG encoding)            │
│  - Live sign translation interface                  │
│  - Socket.IO real-time chat                         │
│  - Education module (pose-viewer + stickman)        │
└────────────────────┬────────────────────────────────┘
                     │ HTTPS / REST / WebSocket
┌────────────────────▼────────────────────────────────┐
│  APPLICATION TIER (Node.js + Express)               │
│  - JWT authentication (bcryptjs + JSON Web Tokens)  │
│  - Prisma ORM → SQLite database                     │
│  - /predict proxy gateway (hides ML tier)           │
│  - Socket.IO server (real-time chat)                │
└────────────────────┬────────────────────────────────┘
                     │ Internal HTTP POST
┌────────────────────▼────────────────────────────────┐
│  INFERENCE TIER (FastAPI, Python)                   │
│  - asl_mlp_inference.py     → ASL Letters           │
│  - arsl_mlp_inference.py    → ArSL Letters          │
│  - en_word_inference.py     → ASL Words (I3D)       │
│  - arsl_word_inference.py   → ArSL Words (BiLSTM)   │
│  - pose_concat.py           → Education animations  │
└─────────────────────────────────────────────────────┘
```

**Data flow:** Webcam frame → base64 JPEG → Node.js (JWT auth) → FastAPI (MediaPipe + model) → JSON prediction → UI display.

---

## 🌟 Key Features

- **Real-time Sign Recognition:** Four modes — ASL/ArSL × Letters/Words — from a standard webcam
- **Authenticated Chat:** JWT-secured login/registration; Socket.IO live chat where sign predictions can be sent as messages
- **Education Module (Part B):** Three bilingual learning tools:
  - **Sign Viewer** — browse categorised vocabulary and watch motion-capture skeleton animations of real signers
  - **Sentence Builder** — type any sentence; dictionary words are signed and unknown words are fingerspelled, with live chip previews
  - **Practice Mode** — perform a prompted sign; the same recognition models check your attempt and give constructive feedback
- **Privacy-preserving inference:** Letter and ArSL-word paths transmit only compact landmark vectors (not raw video) to the server
- **Responsive Design:** Dark mode support, CSS Grid layout adapts from desktop to mobile

---

## 📊 Real-Time Performance

Measured on graduation development hardware (Windows 11, Chrome, 720p webcam, localhost stack, 100 samples/row):

| Component | p50 | p95 |
|---|---|---|
| MediaPipe extraction (server-side) | 34 ms | 48 ms |
| Letter MLP inference | 4 ms | 7 ms |
| ArSL Word BiLSTM inference | 24 ms | 38 ms |
| ASL Word I3D inference (CUDA) | 92 ms | 128 ms |
| **End-to-end letter** | **51 ms** ✅ | 74 ms |
| **End-to-end ASL word** | **108 ms** ✅ | 145 ms |

Letter mode comfortably satisfies the ≤200 ms hypothesis stated in Chapter 1 of the thesis.

---

## 📚 Datasets Used

| Model | Dataset | Size |
|---|---|---|
| ASL Letters | ASL Alphabet (Kaggle `grassknoted/asl-alphabet`) | ~87,000 images, 29 classes |
| ArSL Letters | ArASL2018 (Mendeley) | 54,049 images, 32 classes |
| ASL Words | WLASL-2000 (Li et al. 2020), 100-class subset | RGB video clips |
| ArSL Words | KArSL-502 (Sidig et al. 2021), SignID 71–170 | 100 classes, 2,400 test samples |

---

## 📁 Application Folder Details

### `application/frontend/` — React + Vite
The main Single Page Application. Uses vanilla CSS with CSS custom properties (no Tailwind/Bootstrap), `react-router-dom` for navigation, and React Context for global auth/theme state.

### `application/backend/` — Node.js + Express
The secure middleware between the UI and the AI. Handles JWT auth, Prisma ORM (SQLite), Socket.IO chat, and proxies all `/predict` requests to FastAPI — the ML ports are never exposed to the public internet.

### `application/model-services/` — FastAPI
The AI engine. Dispatches requests by `language` + `mode` to the correct inference module. Also hosts the Education module's pose concatenation pipeline (`pose_concat.py`) with server-side animation stitching, DTW-based sign verification, and `sign.mt` dictionary integration.

### `application/education_module/` — Education Components
An extracted showcase of the custom Canvas2D legacy rendering engine and the React components that power the Education tab. See `education_module/README.md` for full detail.

### `4_Final_Models/` — Training Artifacts
Standalone Jupyter notebooks, pre-trained weights (`.h5` / `.pt`), and vocabulary files for all four models. These are research-reproducibility artifacts; the deployed inference code lives in `model-services/`.

---

## 📄 Thesis

The full thesis (9 chapters, ~145 pages) is included in `application/docs/`. It covers system design (Ch. 5), model methodology (Ch. 3–4), experimental results (Ch. 6), and discussion (Ch. 7).

---

## 🎓 Project Info

- **Project Title:** A Bilingual Sign Language Recognition and Communication System
- **Subtitle:** Real-Time Letter and Word Recognition with a Web-Based Deployment
- **Institution:** Arab Academy for Science, Technology and Maritime Transport (AASTMT)
- **Department:** Computer Engineering
- **Degree:** B.Sc. Final Year Project
- **Date:** July 2026
