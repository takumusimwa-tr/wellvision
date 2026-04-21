# WellVision — Subsurface Lithology Classifier from Well Logs

> An end-to-end ML system that predicts subsurface rock formations from
> wireline well log measurements — built on the FORCE 2020 Norwegian Sea
> dataset used in a real industry ML competition.

**Live demo:** *(coming soon)*

---

## Why this project exists

Every metre drilled underground costs money. Knowing what rock formation
you're drilling through — sandstone, shale, limestone — determines
drilling parameters, completion strategy, and ultimately whether a well
is economically viable.

Traditionally, lithology interpretation requires a trained petrophysicist
manually reading log curves. This project automates that process using
machine learning, trained on 118 wells from the Norwegian Sea with
interpretations made by professional geoscientists.

Built by a Mining Engineer and Radiation Technician who has physically
run gamma-ray spectroscopy tools down boreholes at Wireline Africa,
Mozambique — the sensors in this dataset are the same instruments used
in the field.

---

## Model performance

| Model | Accuracy | Notes |
|---|---|---|
| XGBoost baseline | TBD | benchmark target: 95% (literature) |
| 1D CNN (depth sequences) | TBD | sequence-aware classifier |

---

## Dataset

| Property | Value |
|---|---|
| Source | FORCE 2020 ML Competition |
| Wells | 118 LAS files (Norwegian Sea, Viking Graben) |
| Samples | 1,431,242 labelled depth points |
| Raw features | 20+ well log curves |
| Engineered features | 41 (petrophysical derived + rolling statistics) |
| Target | 11 lithofacies classes |
| License | NOLD 2.0 / CC-BY-4.0 |
| Download | https://zenodo.org/records/4351156 |

### Lithofacies classes (11)
Sandstone, Sandstone/Shale, Shale, Marl, Dolomite,
Limestone, Chalk, Halite, Anhydrite, Tuff, Basement.

> **Note on Coal:** Coal (code 26000) appears in the FORCE 2020 competition
> description but is absent from all 118 wells in this dataset — geologically
> consistent with the Norwegian North Sea formations. Code 93000 (141 samples,
> unknown origin) was dropped as too rare to train on reliably.

### Class distribution
| Lithofacies | Samples | % |
|---|---|---|
| Shale | 877,043 | 61.3% |
| Sandstone | 207,704 | 14.5% |
| Sandstone/Shale | 180,820 | 12.6% |
| Limestone | 69,498 | 4.9% |
| Marl | 41,038 | 2.9% |
| Tuff | 17,431 | 1.2% |
| Halite | 14,712 | 1.0% |
| Chalk | 14,043 | 1.0% |
| Basement | 4,754 | 0.3% |
| Dolomite | 2,391 | 0.2% |
| Anhydrite | 1,808 | 0.1% |

---

## Project structure

```
wellvision/
├── data/
│   ├── raw/
│   │   └── force2020/                  ← 118 LAS files (downloaded)
│   └── processed/
│       ├── figures/                    ← 9 EDA and feature figures
│       ├── features_labelled.parquet   ← 1.4M × 41 feature matrix
│       └── feature_metadata.json       ← feature names, class map
│
├── notebooks/
│   ├── 01_eda.ipynb                    ← Well log viz, class distribution
│   ├── 02_feature_engineering.ipynb    ← Petrophysical features, imputation
│   ├── 03_xgboost_classifier.ipynb     ← XGBoost + RF baseline
│   └── 04_1d_cnn.ipynb                 ← Depth-sequence 1D CNN
│
├── models/
│   ├── lithology_classifier/           ← XGBoost model + metadata
│   └── sequence_classifier/            ← 1D CNN model + metadata
│
├── config.py                           ← Shared paths, class maps, constants
├── api/main.py                         ← FastAPI: /predict /well /health
├── dashboard/app.py                    ← Streamlit well log viewer
├── scripts/download_datasets.py        ← Zenodo downloader (no auth needed)
├── requirements.txt
└── README.md
```

---

## Quickstart

### 1. Clone and install

```powershell
git clone https://github.com/takumusimwa-tr/wellvision.git
cd wellvision
pip install -r requirements.txt
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

### 2. Download dataset

```powershell
python scripts/download_datasets.py
```

Downloads 170 MB zip from Zenodo and extracts 118 LAS files.
No Kaggle account or authentication required.

### 3. Run notebooks in order

```
01_eda.ipynb                  → EDA: 118 wells, curve availability, crossplots
02_feature_engineering.ipynb  → 41 petrophysical + rolling features
03_xgboost_classifier.ipynb   → XGBoost baseline classifier
04_1d_cnn.ipynb               → 1D CNN depth-sequence classifier
```

---

## Engineered features (41 total)

| Category | Features |
|---|---|
| Raw log curves | GR, RHOB, NPHI, RDEP, RMED, DTC, CALI, DRHO |
| Log-transformed | LOG_RDEP, LOG_RMED, RES_RATIO |
| Petrophysical derived | VSHALE, PHID, PHIN, PHITOTAL, AI |
| Depth | DEPTH_ABS, DEPTH_NORM |
| Spatial | X_LOC, Y_LOC, Z_LOC |
| Rolling (5-sample ~0.75m) | GR, RHOB, NPHI, RDEP, VSHALE — mean + std |
| Rolling (21-sample ~3m) | GR, RHOB, NPHI, RDEP, VSHALE — mean + std |

---

## Key engineering context

Wireline well logging measures physical properties of rock formations
at depth using tools lowered into a borehole on a cable. Key sensors:

- **Gamma Ray (GR):** measures natural radioactivity. Shales are radioactive
  (high GR); clean sandstones and carbonates are not (low GR).
- **Bulk Density (RHOB):** denser rocks (limestone, dolomite) read higher.
- **Neutron Porosity (NPHI):** sensitive to hydrogen content — high in
  porous formations.
- **Resistivity (RMED/RDEP):** tight rocks and evaporites resist current.
  Halite shows extreme resistivity — highly distinctive.
- **Acoustic Impedance (AI = RHOB × Vp):** computed from RHOB and DTC.
  Tight carbonates have AI > 10,000; clean sands 6,000–8,000.
- **Vshale:** linear gamma ray index normalised per well (P5/P95 endpoints).
  Industry-standard shale volume estimator.

The RHOB-NPHI density-neutron crossplot is the classic petrophysicist
tool for lithology discrimination — in use since the 1970s. This project
learns equivalent relationships across 41 dimensions simultaneously.

---

## Tech stack

| Layer | Technology |
|---|---|
| Data | pandas, numpy, lasio, scipy |
| Models | XGBoost, LightGBM, scikit-learn, PyTorch (1D CNN) |
| API | FastAPI, Pydantic, Uvicorn |
| Dashboard | Streamlit, Plotly |
| MLOps | MLflow, Docker, GitHub Actions |

---

## Background

Built by **Takudzwa Musimwa** — Mining Engineering BEng
(Midlands State University, 2023) + Data Science MSc candidate
(Pace University, expected 2027).

Field experience: gamma-ray spectroscopy across 50+ well logging
operations at Wireline Africa, Mozambique (2023–2025).

---

## License

MIT