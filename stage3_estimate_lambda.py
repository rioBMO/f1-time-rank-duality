"""
Stage 3: Estimate lambda parameters by minimizing RSS between target p_norm
and lambda/sum(lambda). This implements the grouped parametrization similar
with lambdaest4 in the R code.
Input: output/stage2_probabilities.csv
Output: output/stage3_lambda.csv
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from config import STAGE2_OUT, STAGE3_OUT
from utils import save_df


def objective_grouped(x, target_sorted, counts):
    lambda_sorted = np.repeat(x, counts)
    pred = lambda_sorted / np.sum(lambda_sorted)
    return np.sum((target_sorted - pred)**2)


def run_stage3(input_path=STAGE2_OUT, output_path=STAGE3_OUT):
    print('Stage 3: estimating lambda from', input_path)
    df = pd.read_csv(input_path)
    if 'p_norm' not in df.columns:
        raise ValueError('Expected p_norm in input')
    
    target = df['p_norm'].values
    
    # Implement R's lambdaest4 approach: grouped optimization
    # Sort target and compute run-lengths of unique values
    target_sorted = np.sort(target)
    unique_vals, counts = np.unique(target_sorted, return_counts=True)
    
    print(f"Found {len(unique_vals)} unique probability values:")
    for i, (val, count) in enumerate(zip(unique_vals, counts)):
        print(f"  Group {i+1}: p={val:.9f}, count={count}")
    
    # Initial guess: use unique_vals scaled by empirical factor
    # From R code analysis: lambda values are much smaller than probabilities
    x0 = np.maximum(unique_vals * 0.256, 1e-8)  # Scale factor from journal
    
    # Bounds: all lambda values must be positive
    bounds = [(1e-12, None)] * len(x0)
    
    # Optimize using grouped approach
    res = minimize(objective_grouped, x0, args=(target_sorted, counts), 
                   method='L-BFGS-B', bounds=bounds,
                   options={'maxiter': 10000})
    
    if not res.success:
        print('Warning: optimization did not converge:', res.message)
        # Fallback: use the initial guess
        x_opt = x0
    else:
        x_opt = res.x
        print(f'Optimization converged with error: {res.fun:.2e}')
    
    # Reconstruct full lambda vector aligned with original driver order
    # Create mapping: for each target value, find index in unique_vals
    idx_map = []
    for v in target:
        idx = np.where(np.abs(unique_vals - v) < 1e-12)[0][0]
        idx_map.append(idx)
    
    lambda_full = np.array([x_opt[i] for i in idx_map], dtype=float)
    
    # Verify solution quality
    lambda_sum = np.sum(lambda_full)
    predicted_probs = lambda_full / lambda_sum
    errors = np.abs(target - predicted_probs)
    max_error = np.max(errors)
    mean_error = np.mean(errors)
    
    print(f'Lambda sum: {lambda_sum:.10f}')
    print(f'Max probability error: {max_error:.2e}')
    print(f'Mean probability error: {mean_error:.2e}')
    
    # Create output dataframe
    out_df = df.copy()
    out_df['lambda_est'] = lambda_full
    out_df['p_predicted'] = predicted_probs
    out_df['p_error'] = errors
    
    # Display grouped lambda values (like R output)
    print(f"\nGrouped Lambda Values (like R's x1 output):")
    for i, (val, lam) in enumerate(zip(unique_vals, x_opt)):
        print(f"  Group {i+1}: p={val:.9f} -> lambda={lam:.10f}")
    
    # Display results for key drivers
    print(f"\nKey Results Comparison with Journal:")
    key_drivers = ['Max Verstappen', 'Lewis Hamilton', 'Sergio Perez', 'Fernando Alonso']
    for driver in key_drivers:
        driver_rows = out_df[out_df['Driver'] == driver]
        if len(driver_rows) > 0:
            row = driver_rows.iloc[0]
            print(f"{driver:15s}: p_norm={row['p_norm']:.9f}, lambda={row['lambda_est']:.10f}")
    
    save_df(out_df, output_path)
    print('Stage 3 done. Wrote ->', output_path)
    return out_df

if __name__ == '__main__':
    run_stage3()