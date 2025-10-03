import re
import numpy as np
import pandas as pd
from scipy.stats import norm

from config import ROOT


def fractional_to_rawprob(s):
    """Convert fractional or decimal odds string to raw implied probability.
    Handles formats like '25/1', '2/9', '1.5', 'EVS' (even -> 1/2).
    Returns np.nan if cannot parse.
    """
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    # handle common words
    if s.upper() in ('EVEN','EVS','EVENS'):
        return 1.0 / 2.0
    # fractional
    if '/' in s:
        parts = s.split('/')
        try:
            a = float(parts[0])
            b = float(parts[1])
            return b / (a + b)
        except Exception:
            return np.nan
    # decimal
    try:
        d = float(s)
        if d <= 0:
            return np.nan
        return 1.0 / d
    except Exception:
        return np.nan


def save_df(df, path, index=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)
