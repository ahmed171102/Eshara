# Frontend — React + Vite Client Tier

This is the **Client Tier** of the Eshara three-tier architecture, as documented in **Chapter 5, Section 5.2** of the thesis. It is a Single Page Application (SPA) built with React and bundled with Vite.

## Key Features

- **Real-time Sign Translation:** Captures webcam frames as base64 JPEG and sends them to the backend `/predict` endpoint
- **Four recognition modes:** ASL Letters, ArSL Letters, ASL Words, ArSL Words (controlled by `language` + `mode` dropdowns)
- **Live Chat (Socket.IO):** Authenticated users can send sign translations directly into a real-time chat room
- **Education Module:** Three bilingual learning tools — Sign Viewer (motion-capture skeleton animations), Sentence Builder (free-text to signed animation), and Practice mode (webcam-based sign checking)
- **Authentication:** JWT-based login/register with an Axios interceptor that attaches `Authorization: Bearer` on every outbound request and redirects to login on 401
- **Theming:** Dark/light mode via a root-level `data-theme` attribute and CSS custom properties (no Tailwind/Bootstrap)

## Application Pages

- **Landing Page** — public-facing entry point with login/register tabs, Eshara logo, and dark mode toggle
- **App Home Page** — authenticated users only (protected by `ProtectedRoute`); split into **Chatting** tab and **Educational** tab

## Structure

```
src/
├── App.jsx              Root component + routing (react-router-dom)
├── main.jsx             Vite entry point
├── index.css            Global CSS design system (tokens, typography, layout)
├── App.css              App-level styles
├── pages/               Top-level page views (LandingPage, AppHomePage, etc.)
├── components/
│   ├── ASLStickman.jsx        Legacy Canvas2D fingerspelling component (A–Z)
│   ├── ASLWordStickman.jsx    Legacy Canvas2D word-sign component (IK solver)
│   ├── ProtectedRoute.jsx     JWT route guard HOC
│   └── education/
│       ├── PracticePanel.jsx  Webcam practice mode UI
│       └── SentenceBuilder.jsx Free-text signing UI
├── context/
│   ├── AuthContext.jsx    Global auth state (JWT storage + user session)
│   └── ThemeContext.jsx   Dark/light mode state
├── services/              Axios API helpers (auth, predict calls)
└── utils/
    ├── aslRenderer.js     Custom dependency-free Canvas2D rendering engine
    ├── aslHandPoses.js    Procedural MediaPipe-compatible hand pose data (A–Z)
    ├── aslWordPoses.js    Keyframed IK-driven word sign animation data
    ├── arslWords.js       ArSL word vocabulary helpers
    ├── poseViewer.js      pose-viewer web component wrapper
    ├── practiceMatch.js   Answer matching logic (with Arabic orthography folding)
    └── useCamera.js       Shared webcam capture hook
```

## Setup

```bash
npm install
npm run dev
```

Runs at **http://localhost:5173**
