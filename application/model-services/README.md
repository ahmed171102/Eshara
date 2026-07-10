# Model Services — FastAPI AI Inference Server

This is the **Inference Tier** of the Eshara three-tier architecture. It is a FastAPI (Python) server that hosts all four sign language recognition models behind a single `/predict` endpoint. It is accessed internally by the Node.js backend — it is never directly exposed to the public internet.

## The Four Inference Modules

| File | Model | Language | Mode | Input | Output |
|---|---|---|---|---|---|
| `asl_mlp_inference.py` | ASL Letter MLP | English | Letters | 78-D engineered MediaPipe hand landmarks | A–Z + space + del (28 classes) |
| `arsl_mlp_inference.py` | ArSL Letter MLP | Arabic | Letters | 63-D raw MediaPipe hand landmarks | 32 Arabic letters |
| `en_word_inference.py` | ASL Word Inception I3D | English | Words | 32-frame × 224×224 RGB clips (per-session stateful buffer) | WLASL-100 gloss |
| `arsl_word_inference.py` | ArSL Word BiLSTM | Arabic | Words | 225-D Holistic landmarks × 48 frames | KArSL Arabic word |

## Key Files

| File | Purpose |
|---|---|
| `app.py` | Main FastAPI app — request routing by `language` + `mode` |
| `asl_pipeline.py` | Shared MediaPipe Holistic processing pipeline |
| `pytorch_i3d.py` | Inception I3D model architecture definition (PyTorch) |
| `pose_concat.py` | Education module: server-side animation stitching + DTW verification |
| `fetch_signmt_pose.py` | Offline script to fetch `.pose` files from the sign.mt dictionary API |
| `requirements.txt` | All Python dependencies |
| `models/` | Directory for trained model weight files (`.h5` and `.pt`) |
| `poses/` | Cached `.pose` animation files for the Education module |

## Request Contract

All four models share a single request schema:

```json
{
  "language": "en | ar",
  "mode": "letters | words",
  "imageBase64": "<base64-encoded JPEG frame>",
  "sessionId": "<user-id for ASL word stateful buffering>"
}
```

## Performance (from thesis Chapter 5, Table 5-latency)

| Path | p50 | p95 |
|---|---|---|
| MediaPipe extraction (server-side) | 34 ms | 48 ms |
| Letter MLP forward pass | 4 ms | 7 ms |
| ArSL Word BiLSTM (48-frame batch) | 24 ms | 38 ms |
| ASL Word I3D (32-frame, CUDA) | 92 ms | 128 ms |

## Setup

```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Runs at **http://localhost:8000** (internal only, proxied via Node.js backend)
