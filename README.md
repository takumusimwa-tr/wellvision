# WellVision — Subsurface Lithology Classifier from Well Logs

> An end-to-end ML system that predicts subsurface rock formations from
> wireline well log measurements — built on the FORCE 2020 Norwegian Sea
> dataset used in a real industry ML competition.

**Live demo:** *(coming soon)*

---

## Why this project exists

Every metre drilled underground costs money. Knowing what rock formation
you're drilling through — sandstone, shale, limestone, coal — determines
drilling parameters, completion strategy, and ultimately whether a well
is economically viable.

Traditionally, lithology interpretation requires a trained petrophysicist
manually reading log curves. This project automates that process using
machine learning, trained on 98 wells from the Norwegian Sea with
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
| Wells | 118 total (98 train, 10 open test, 10 blind test) |
| Samples | ~1.17M depth points |
| Features | 26 well log measurements |
| Target | 12 lithofacies classes |
| License | NOLD 2.0 |
| Download | https://zenodo.org/records/4351156 |

### Well log features
GR (gamma ray), RHOB (bulk density), NPHI (neutron porosity),
DTC (compressional slowness), DTS (shear slowness),
RMED/RDEP (resistivity), PEF (photoelectric factor),
CALI (caliper), SP (spontaneous potential),
and stratigraphic/positional features (X, Y, depth, group).

### Lithofacies classes
Sandstone, Sandstone/Shale, Shale, Marl, Dolomite,
Limestone, Chalk, Halite, Anhydrite, Tuff,
Coal, Basement.

---

## Project structure

```
wellvision/
├── data/
│   ├── raw/
│   │   └── force2020/        ← FORCE 2020 CSVs (downloaded)
│   └── processed/            ← Feature-engineered data + figures
│
├── notebooks/
│   ├── 01_eda.ipynb                  ← Well log visualisation, lithofacies distribution
│   ├── 02_feature_engineering.ipynb  ← Petrophysical derived features
│   ├── 03_xgboost_classifier.ipynb   ← XGBoost + RF baseline
│   └── 04_1d_cnn.ipynb               ← Depth-sequence 1D CNN
│
├── models/
│   ├── lithology_classifier/   ← XGBoost/RF model + metadata
│   └── sequence_classifier/    ← 1D CNN model + metadata
│
├── api/
│   └── main.py                 ← FastAPI: /predict /well /health
│
├── dashboard/
│   └── app.py                  ← Streamlit well log viewer
│
├── scripts/
│   └── download_datasets.py    ← Zenodo downloader
│
├── tests/
├── .github/workflows/ci.yml
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

Downloads train.csv (~150 MB) and test.csv from Zenodo. No authentication required.

### 3. Run notebooks in order

```
notebooks/01_eda.ipynb                 → EDA and well log visualisation
notebooks/02_feature_engineering.ipynb → Petrophysical features
notebooks/03_xgboost_classifier.ipynb  → Baseline classifier
notebooks/04_1d_cnn.ipynb              → 1D CNN sequence classifier
```

---

## Key engineering context

Wireline well logging measures physical properties of rock formations
at depth using tools lowered into a borehole on a cable. The key sensors:

- **Gamma Ray (GR):** measures natural radioactivity. Shales are radioactive
  (high GR); clean sandstones and carbonates are not (low GR). The single
  most diagnostic lithology indicator.
- **Bulk Density (RHOB):** denser rocks (limestone, dolomite) read higher.
  Coal reads very low (~1.3 g/cc) making it highly distinctive.
- **Neutron Porosity (NPHI):** sensitive to hydrogen content — high in
  porous formations and coal.
- **Resistivity (RMED/RDEP):** hydrocarbons and tight rocks resist current;
  saltwater-saturated formations conduct it. Distinguishes fluid types.
- **Photoelectric Factor (PEF):** highly sensitive to mineralogy, especially
  useful for distinguishing carbonate types.

The crossplot of RHOB vs NPHI is the classic lithology identification
technique used by petrophysicists since the 1970s. Machine learning
can learn these relationships across 26 dimensions simultaneously.

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
