# ArSL Letter Recognition — Arabic Letters Model

**Task:** Real-time recognition of Arabic Sign Language (ArSL) finger-spelled letters from a standard webcam.  
**Architecture:** Multi-Layer Perceptron (MLP) over raw MediaPipe hand landmarks.  
**Final Accuracy:** **99.63% Top-1 / 99.44% Macro-F1** (14,734 test samples)

---

## Files

| File | Description |
|---|---|
| `MediaPipe_ARLetters_training.ipynb` | Canonical training pipeline — landmark extraction, MLP training, full evaluation |
| `Production_Architecture_Arabic.ipynb` | Clean, finalised production architecture notebook |
| `arsl_mediapipe_mlp_model_bestV2.2.h5` | **Trained model weights** (2.2 MB) — loaded by `model-services/arsl_mlp_inference.py` at runtime |
| `ASLAD-3000_v2.csv` | Extracted 63-D MediaPipe landmark dataset used for training (91 MB) |

---

## Model Specification

| Property | Value |
|---|---|
| **Input features** | 63-D **raw** MediaPipe Hand landmarks (21 points × 3 coordinates, no additional engineering) |
| **Architecture** | MLP wider head: 512 → 256 → 64 → 32 softmax |
| **Deployed classes** | **32** Arabic letters |
| **Source corpus** | ArASL2018 (Mendeley, 54,049 images, 32 classes) |
| **Normalisation** | Internal BatchNorm only — no external StandardScaler |
| **Parameters** | ~183k |

---

## Web Inference

This model is served live via `application/model-services/arsl_mlp_inference.py`. The web app applies the same real-time stabilisation as the English letter model:
- **Buffer:** 10-frame sliding window
- **Vote threshold:** 7/10 majority vote required to commit a prediction
- **Hold time:** 0.8-second cooldown between commits

> The ArSL letter model uses raw 63-D coordinates (not engineered features like the ASL model) because the ArASL2018 dataset's inter-class separation is high enough that raw coordinates achieve state-of-the-art accuracy without additional feature engineering.
