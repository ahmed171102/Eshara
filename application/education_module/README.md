# Education Module — Bilingual Sign-Language Learning

This folder is an **extracted showcase** of the Education Module source files, as documented in **Chapter 5, Section 5.14 (Part B)** of the thesis. These files are actively imported and used within the main `frontend/src` application — this directory exists purely so reviewers can find and evaluate them without searching through the full React project.

> The current deployed Education tab uses the **`pose-viewer` web component** with motion-capture skeleton recordings from real signers (`.pose` format). The Canvas2D engine in this folder is the **legacy iteration** — it remains as a fallback renderer for English words that have hand-authored keyframes but no `.pose` file.

---

## Files

### The Legacy Canvas2D Rendering Engine
| File | Description |
|---|---|
| `aslRenderer.js` | **Dependency-free Canvas2D rendering engine.** Draws 21-point MediaPipe-compatible hand topologies. Contains the two-joint analytic IK solver (`solveArm`) with frame-to-frame elbow-hint continuity for smooth arm movement. |
| `aslHandPoses.js` | Procedurally-constructed MediaPipe-compatible hand pose coordinates for all A–Z fingerspelling letters. Special-cases J and Z for in-air motion. |
| `aslWordPoses.js` | Keyframed animation data for 15 word signs (COME, DRINK, EAT, GO, HELLO, HELP, LEARN, MORE, NAME, NO, PLEASE, SORRY, STOP, WATER, YES) driven by the IK solver. |

### React Components
| File | Description |
|---|---|
| `ASLStickman.jsx` | React component wrapping `aslRenderer.js` for A–Z fingerspelling. Morphs between hand poses at 260 ms per letter with a 620 ms hold. |
| `ASLWordStickman.jsx` | React component that plays keyframed word sign animations via the IK solver. |

### Education Tab UI Components
| File | Description |
|---|---|
| `PracticePanel.jsx` | The webcam-based practice mode UI. Reuses the shared `useCamera` hook and the `/predict` endpoint to check the learner's sign. Provides constructive feedback including best-guess confidence and hand configuration hints. |
| `SentenceBuilder.jsx` | The free-text sentence builder UI. Tokenises input, shows live solid/dashed chip previews (signed vs. spelled), and triggers the server-side `pose_concat` stitching pipeline. |

---

## Why Two Rendering Approaches?

The Education module went through a major rebuild documented in Section 5.14.2 of the thesis:

| | **Legacy Canvas2D (this folder)** | **Deployed motion-capture** |
|---|---|---|
| Rendering | Hand-authored keyframes + IK stick figure | `<pose-viewer>` skeleton from `.pose` recordings of real signers |
| Vocabulary | 15 word signs (ASL only) | 44 EN + 22 AR words + both alphabets |
| Multi-sign playback | Client-side sequencing (choppy) | One server-stitched animation with metadata timing |
| Correctness | Manual geometric review | DTW fallback detection + filmstrip review + Playwright browser tests |

The root cause of the original choppy playback was **client-side per-clip fetching**, not the renderer itself. Fixing it required moving animation assembly to the server (`pose_concat.py`), which also unlocked real human motion data and bilingual (ASL + ArSL) coverage without manual animation work.
