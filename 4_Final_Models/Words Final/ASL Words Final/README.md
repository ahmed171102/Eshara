# ASL Word Recognition — English Words Model

**Task:** Recognition of 100 American Sign Language (ASL) isolated word signs from webcam video clips.  
**Architecture:** Inception I3D (Inflated 3D ConvNet) — PyTorch.  
**Benchmark Accuracy:** **65.89% Top-1 / 84.11% Top-5** (Li et al. 2020 WLASL-100 I3D benchmark)

---

## Files

| File | Description |
|---|---|
| `ASL_Word_Training.ipynb` | Training pipeline notebook for the BiLSTM-based landmark word recognition experiment (research artifact; deployed model uses I3D) |
| `asl_word_lstm_model_best.h5` | Best LSTM model weights from the landmark-based training experiments (6 MB) |
| `asl_word_classes.csv` | Vocabulary list mapping class indices to ASL word glosses |

---

## Model Specification (Deployed — Inception I3D)

| Property | Value |
|---|---|
| **Architecture** | Inception I3D — pretrained RGB 3D ConvNet with a 100-way WLASL classification head |
| **Input** | 32 consecutive frames × 224×224 RGB, normalised to [−1, 1] |
| **Preprocessing** | Short-side resize to 256 px → centre crop 224×224 → normalise |
| **Vocabulary** | 100 WLASL glosses (Li et al. 2020, `nslt_100.json`) |
| **Weights file** | `asl100.pt` / `asl_word_i3d.pt` (stored in `model-services/models/`) |
| **Framework** | PyTorch |

---

## Web Inference Stabilisation

The I3D model is served via `application/model-services/en_word_inference.py` with **stateful per-session buffering**:
- **Frame buffer:** 32-frame deque per `session_id` (one per authenticated user)
- **Voting window:** 10 predictions; class committed when ≥ 6/10 majority + ≥ 50% confidence
- **Cooldown:** 1.2-second minimum between commits
- **Latency:** p50 = 92 ms for I3D inference (CUDA); end-to-end p50 = **108 ms**

---

## Important Notes

The BiLSTM model in this folder (`asl_word_lstm_model_best.h5`) is a **research artifact** from an earlier landmark-based experiment (462-D MediaPipe Holistic, 30 frames, 157-class subset). It is documented in the thesis (Chapter 6, superseded models table) but **is not the deployed graduation model**.

The deployed web model is the **Inception I3D** (`asl100.pt`) which was integrated on the `add-wlasl-model` branch and merged into the final `application/` codebase. The accuracy figures cited (65.89% / 84.11%) are from the **Li et al. 2020 WLASL-100 benchmark** — the same I3D checkpoint evaluated on the same test split.
