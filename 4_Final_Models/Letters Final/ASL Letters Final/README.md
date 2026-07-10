# ASL Letter Recognition — English Letters Model

**Task:** Real-time recognition of American Sign Language (ASL) finger-spelled letters from a standard webcam.  
**Architecture:** Multi-Layer Perceptron (MLP) over engineered MediaPipe hand landmarks.  
**Final Accuracy:** **99.06% Top-1 / 98.74% Macro-F1** (12,401 test samples)

---

## Files

| File | Description |
|---|---|
| `MLFlow_Script.ipynb` | Canonical training pipeline — data loading, 78-D feature engineering, MLP training, MLflow experiment tracking |
| `Production_Architecture_English.ipynb` | Clean, finalized production architecture notebook |
| `asl_mediapipe_mlp_model_engineered.h5` | **Trained model weights** (2.5 MB) — loaded by `model-services/asl_mlp_inference.py` at runtime |
| `asl_letters_engineered.csv` | Extracted 78-D MediaPipe landmark dataset used for training (54 MB) |

---

## Model Specification

| Property | Value |
|---|---|
| **Input features** | 78-D engineered MediaPipe Hand landmarks (wrist-relative normalisation + 15 joint angles) |
| **Architecture** | 3-hidden-layer MLP: 256 → 128 → 64 → 28 softmax |
| **Deployed classes** | **28** (A–Z + `space` + `del`; `nothing` class excluded from web deployment) |
| **Source corpus** | ASL Alphabet (Kaggle `grassknoted/asl-alphabet`, ~87,000 images, 29 classes) |
| **Normalisation** | Internal BatchNorm only — no external StandardScaler |

---

## Web Inference

This model is served live via `application/model-services/asl_mlp_inference.py`. The web app applies real-time stabilisation:
- **Buffer:** 10-frame sliding window
- **Vote threshold:** 7/10 majority vote required to commit a prediction
- **Hold time:** 0.8-second cooldown between commits

> **Note:** Server-side MediaPipe extraction dominates the letter-path compute budget (p50 = 34 ms). MLP forward pass itself is under 5 ms on CPU. End-to-end letter inference p50 = **51 ms** (well within the ≤200 ms target from Chapter 1 of the thesis).
