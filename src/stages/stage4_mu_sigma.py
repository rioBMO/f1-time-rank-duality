"""
Stage 4: Compute sigma and mu_i from p_norm using normal quantile mapping:
    z_i = Phi^{-1}(p_i)
    sigma = (1.5*n - n(n+1)/2) / sum(z_i)
    mu_i = 1.5 - sigma * z_i
Input: output/stage2_probabilities.csv or stage3 output (we use p_norm)
Output: output/stage4_mu_sigma.csv
"""
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
from scipy.stats import norm
from config import STAGE2_OUT, STAGE4_OUT
from utils import save_df


def run_stage4(input_path=STAGE2_OUT, output_path=STAGE4_OUT):
    print('Stage 4: computing mu and sigma from p_norm in', input_path)
    df = pd.read_csv(input_path)
    if 'p_norm' not in df.columns:
        raise ValueError('Expected p_norm in input')
    p = df['p_norm'].values.astype(float)
    n = len(p)
    # handle edge probabilities near 0 or 1
    eps = 1e-12
    p_clipped = np.clip(p, eps, 1-eps)
    z = norm.ppf(p_clipped)
    sigma_hat = (1.5 * n - n*(n+1)/2.0) / z.sum()
    mu_hat = 1.5 - sigma_hat * z
    out = df.copy()
    out['z'] = z
    out['mu_hat'] = mu_hat
    out['sigma_hat'] = sigma_hat
    save_df(out, output_path)
    print('Stage 4 done. Wrote ->', output_path)
    return out

if __name__ == '__main__':
    run_stage4()
