from pathlib import Path

# Project root (parent of src folder)
ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = ROOT / 'data'
OUTPUT_DIR = ROOT / 'output'
LOGS_DIR = ROOT / 'logs'
MODELS_DIR = ROOT / 'models'

# Ensure directories exist
for p in (DATA_DIR, OUTPUT_DIR, LOGS_DIR, MODELS_DIR):
    p.mkdir(parents=True, exist_ok=True)

# Filenames used across stages
STAGE1_IN = DATA_DIR / 'odds_table1.csv'        # expected input for stage 1 (Team,Driver,Odds)
STAGE1_OUT = OUTPUT_DIR / 'stage1_odds_parsed.csv'

STAGE2_OUT = OUTPUT_DIR / 'stage2_probabilities.csv'   # contains raw_implied_p and p_norm

STAGE3_OUT = OUTPUT_DIR / 'stage3_lambda.csv'         # estimated lambda per driver

STAGE4_OUT = OUTPUT_DIR / 'stage4_mu_sigma.csv'       # mu_i and sigma results

STAGE5_IN = DATA_DIR / 'f1seconddata.txt'             # race positions, used by regression stage
STAGE5_OUT = OUTPUT_DIR / 'stage5_regression.csv'     # regression coefficients and stats
