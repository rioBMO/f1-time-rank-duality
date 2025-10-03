"""
Stage 2: Renormalize implied probabilities to remove overround.
Input: output/stage1_odds_parsed.csv
Output: output/stage2_probabilities.csv
"""
import pandas as pd
from config import STAGE1_OUT, STAGE2_OUT
from utils import save_df


def run_stage2(input_path=STAGE1_OUT, output_path=STAGE2_OUT):
    print('Stage 2: renormalizing probabilities from', input_path)
    df = pd.read_csv(input_path)
    if 'raw_implied_p' not in df.columns:
        raise ValueError('Expected raw_implied_p in input')
    sum_raw = df['raw_implied_p'].sum()
    if sum_raw <= 0 or pd.isna(sum_raw):
        raise ValueError('Sum of raw_implied_p is non-positive or NaN')
    df['p_norm'] = df['raw_implied_p'] / sum_raw
    save_df(df, output_path)
    print('Stage 2 done. Wrote ->', output_path)
    return df

if __name__ == '__main__':
    run_stage2()
