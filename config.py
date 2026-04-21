"""
WellVision — shared configuration
All notebooks and scripts import paths from here.
"""
from pathlib import Path

ROOT    = Path(__file__).resolve().parent
DATA    = ROOT / "data"
RAW     = DATA / "raw" / "force2020"
LAS_DIR = RAW / "Force_2020_all_wells_train_test_blind_hidden_final"
PROC    = DATA / "processed"
FIGS    = PROC / "figures"
MODELS  = ROOT / "models"

# Create dirs if missing
for d in [PROC, FIGS, MODELS / "lithology_classifier", MODELS / "sequence_classifier"]:
    d.mkdir(parents=True, exist_ok=True)

# ── FORCE 2020 lithofacies class map ──────────────────────────────────────────
# Integer codes as they appear in FORCE_2020_LITHOFACIES_LITHOLOGY curve
LITH_MAP = {
    30000: "Sandstone",
    65030: "Sandstone/Shale",
    65000: "Shale",
    80000: "Marl",
    74000: "Dolomite",
    70000: "Limestone",
    70032: "Chalk",
    88000: "Halite",
    86000: "Anhydrite",
    99000: "Tuff",
    26000: "Coal",
    90000: "Basement",
}

LITH_COLORS = {
    "Sandstone"       : "#F4D03F",
    "Sandstone/Shale" : "#D4AC0D",
    "Shale"           : "#7F8C8D",
    "Marl"            : "#A9CCE3",
    "Dolomite"        : "#85C1E9",
    "Limestone"       : "#5DADE2",
    "Chalk"           : "#AED6F1",
    "Halite"          : "#F1948A",
    "Anhydrite"       : "#E8DAEF",
    "Tuff"            : "#A9DFBF",
    "Coal"            : "#212121",
    "Basement"        : "#922B21",
}

# Standard log curves present in most wells
STANDARD_CURVES = ["GR", "RHOB", "NPHI", "DTC", "RDEP", "RMED", "PEF",
                   "CALI", "SP", "DRHO", "MUDWEIGHT", "ROP"]

# Curves most reliably present across all 118 wells (used for modelling)
CORE_CURVES = ["GR", "RHOB", "NPHI", "RDEP", "RMED"]

TARGET_COL     = "FORCE_2020_LITHOFACIES_LITHOLOGY"
CONFIDENCE_COL = "FORCE_2020_LITHOFACIES_CONFIDENCE"
WELL_COL       = "WELL"
DEPTH_COL      = "DEPTH_MD"
