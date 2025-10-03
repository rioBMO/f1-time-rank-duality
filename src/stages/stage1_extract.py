"""
Stage 1: Read odds CSV (Team,Driver,Odds) and sanitize.
Input expected: data/odds_table1.csv
Output: output/stage1_odds_parsed.csv
"""
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import STAGE1_IN, STAGE1_OUT
from utils import fractional_to_rawprob, save_df


def run_stage1(input_path=STAGE1_IN, output_path=STAGE1_OUT):
    print('Stage 1: reading', input_path)
    # Try different delimiters since the CSV might use semicolon
    try:
        df = pd.read_csv(input_path, sep=';')
    except:
        try:
            df = pd.read_csv(input_path, sep=',')
        except:
            df = pd.read_csv(input_path)
    
    # Clean column names (remove leading/trailing spaces)
    df.columns = df.columns.str.strip()
    
    # Expect columns: Team, Driver, Odds (case-insensitive)
    cols = {c.lower().strip(): c for c in df.columns}
    
    # Normalize column names
    expected = []
    for k in ['team','driver']:
        if k in cols:
            expected.append(cols[k])
        else:
            raise ValueError(f"Input file {input_path} must contain column '{k}' (found: {list(df.columns)})")
    
    # Handle odds column with different possible names
    odds_col = None
    for odds_name in ['odds', 'bookmakers odds', 'bookmaker odds']:
        if odds_name in cols:
            odds_col = cols[odds_name]
            break
    
    if odds_col is None:
        raise ValueError(f"Input file {input_path} must contain odds column (found: {list(df.columns)})")
    
    expected.append(odds_col)
    
    df = df[expected].copy()
    df.columns = ['Team','Driver','Odds']
    
    # Clean data - remove leading/trailing spaces
    df['Team'] = df['Team'].astype(str).str.strip()
    df['Driver'] = df['Driver'].astype(str).str.strip()
    df['Odds'] = df['Odds'].astype(str).str.strip()
    
    # compute raw implied probability
    df['raw_implied_p'] = df['Odds'].apply(fractional_to_rawprob)
    save_df(df, output_path)
    print('Stage 1 done. Wrote ->', output_path)
    return df

if __name__ == '__main__':
    run_stage1()
