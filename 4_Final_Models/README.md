# 4 Final Models — AI Training Artifacts

This directory contains the finalized training notebooks, pre-trained model weights, and datasets for all four Eshara AI models. This is a standalone research archive — the actual deployed inference scripts live in `application/model-services/`.

## Structure

```
4_Final_Models/
├── Letters Final/
│   ├── ASL Letters Final/    # English letter model training + weights
│   └── ArSL Letters Final/   # Arabic letter model training + weights
└── Words Final/
    ├── ASL Words Final/      # English word model training + weights
    └── ArSL Words Final/     # Arabic word model (Issam BiLSTM bundle)
```

## Model Summary

| Folder | Task | Architecture | Top-1 Accuracy |
|---|---|---|---|
| ASL Letters Final | A–Z English letters | MLP (78-D MediaPipe) | **99.06%** |
| ArSL Letters Final | Arabic letters | MLP (63-D MediaPipe) | **99.63%** |
| ASL Words Final | 100 WLASL glosses | Inception I3D | **65.89%** (Li et al. benchmark) |
| ArSL Words Final | 100 Arabic medical words | Stacked BiLSTM (225-D Holistic) | **99.62%** |
