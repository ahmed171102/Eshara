# ArSL Word Recognition — Arabic Words Model (Issam Demo Bundle)

**Task:** Recognition of 100 Arabic Sign Language (KArSL) medical/anatomy isolated word signs.  
**Architecture:** Stacked Bidirectional LSTM on MediaPipe Holistic landmarks (nose/wrist-normalised).  
**Final Accuracy:** **99.62% Top-1** (N=2,400 KArSL test samples)

---

## Files

| File | Description |
|---|---|
| `Holistic_keypoints_BiLSTM_model_3_signers_...h5` | **Trained model weights** (3.1 MB) — the canonical graduation ArSL word model |
| `arsl_issam_demo.py` | Standalone Python inference script for webcam or video file input |
| `bundle_config.py` | Model configuration constants (vocab size, feature dims, frame count) |
| `Issam_Word_Live_Test.ipynb` | Live webcam inference notebook — open this to test the model interactively |
| `Issam_Bundle_Samples_Batch_Test.ipynb` | Batch accuracy validation notebook against KArSL sample videos |
| `Issam_One_Video_Sample.ipynb` | Single-video sanity-check notebook |
| `KARSL-502_Labels.xlsx` | Full KArSL-502 vocabulary label map (502 classes) |
| `requirements.txt` | Python dependencies for running this bundle standalone |
| `sample_videos/` | Reference `.mp4` clips from the KArSL dataset (SignID 71–170) |

---

## Model Specification

| Property | Value |
|---|---|
| **Architecture** | Stacked Bidirectional LSTM (BiLSTM) |
| **Input features** | **225-D** nose/wrist-normalised MediaPipe Holistic landmarks per frame |
| **Feature breakdown** | Pose (33 keypoints) + Left hand (21 keypoints) + Right hand (21 keypoints), normalised relative to body centre (nose + wrist anchors) |
| **Sequence length** | **48 frames** per clip |
| **Vocabulary** | 100 Arabic medical words — KArSL **SignID 71–170** only |
| **Dataset** | KArSL-502 (Sidig et al. 2021) |
| **Training loss** | 0.026 |
| **Trained with** | 3 signers |

---

## Accuracy Results

| Metric | Value |
|---|---|
| Top-1 Accuracy | **99.62%** |
| Validation Accuracy | 99.72% |
| Test samples | 2,400 |
| Training loss | 0.026 |

---

## Web Integration Status

This model is **offline-validated** in the Eshara web application. The trained BiLSTM checkpoint is loaded and tested via `application/model-services/arsl_word_inference.py`, and server-side inference metrics are reported in the thesis (Chapter 5, Table 5-latency: p50 = 24 ms, p95 = 38 ms). However, the live `/predict` endpoint for `arabic + words` currently returns a mock response in the web UI, pending full front-end integration (listed as future work in Chapter 9 of the thesis).

---

## Running This Bundle Standalone

```bash
pip install -r requirements.txt
# Then open and run Issam_Word_Live_Test.ipynb in Jupyter
```
