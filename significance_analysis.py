import pandas as pd
import numpy as np
import statsmodels.api as sm
from stage5_regression import read_positions_matrix

def analyze_statistical_significance():
    """
    Analisis signifikansi statistik untuk memahami stepwise regression
    """
    print("="*80)
    print("ANALISIS SIGNIFIKANSI STATISTIK DALAM STEPWISE REGRESSION")
    print("="*80)
    
    # Load data
    pos, driver_names = read_positions_matrix('data/f1seconddata.txt')
    n_drivers = pos.shape[0]
    n_races = pos.shape[1]
    
    # Prepare data exactly like stage5
    positionlabel = pos.flatten(order='F')
    driverorder_base = np.tile([1, 2], 10)
    driverorder = np.tile(driverorder_base, n_races)
    driverorder2 = driverorder - 1
    
    # Team mapping
    actual_teams = [
        "Mercedes", "Mercedes", "RedBull", "RedBull", "Ferrari", "Ferrari",
        "Mclaren", "Mclaren", "Alpine", "Alpine", "AstonMartin", "AstonMartin",
        "Haas", "Haas", "AlfaTauri", "AlfaTauri", "AlfaRomeo", "AlfaRomeo",
        "Williams", "Williams"
    ]
    constructors = np.tile(actual_teams, n_races)
    
    # Create DataFrame
    df = pd.DataFrame({
        'positionlabel': positionlabel.astype(float),
        'driverorder2': driverorder2.astype(float),
        'constructor': constructors
    })
    
    # Create team dummies (Williams as reference)
    team_dummies = pd.get_dummies(df['constructor'], prefix='', prefix_sep='').astype(float)
    if 'Williams' in team_dummies.columns:
        team_dummies = team_dummies.drop('Williams', axis=1)
    
    print(f"Data prepared: {len(df)} observations")
    print(f"Teams available: {list(team_dummies.columns)}")
    print()
    
    # === MODEL 1: FULL MODEL (9 TEAMS) ===
    print("1. FULL MODEL (SEMUA 9 TIM)")
    print("-" * 50)
    
    X_full = pd.concat([df[['driverorder2']], team_dummies], axis=1)
    X_full = sm.add_constant(X_full)
    y = df['positionlabel']
    
    model_full = sm.OLS(y, X_full).fit()
    
    print("Hasil Signifikansi (α = 0.05):")
    print(f"{'Tim':<15} {'Coefficient':<12} {'Std Error':<12} {'t-value':<10} {'p-value':<12} {'Signifikan?':<12}")
    print("-" * 85)
    
    significance_results = []
    
    for var in model_full.params.index:
        if var == 'const':
            continue
        coef = model_full.params[var]
        stderr = model_full.bse[var]
        t_val = model_full.tvalues[var]
        p_val = model_full.pvalues[var]
        is_significant = "YA" if p_val < 0.05 else "TIDAK"
        
        if var == 'driverorder2':
            var_display = 'Second driver'
        else:
            var_display = var
            
        print(f"{var_display:<15} {coef:<12.4f} {stderr:<12.4f} {t_val:<10.3f} {p_val:<12.4f} {is_significant:<12}")
        
        if var != 'driverorder2':  # Only store team variables
            significance_results.append({
                'team': var,
                'coefficient': coef,
                'p_value': p_val,
                'significant': p_val < 0.05
            })
    
    print(f"\nR² Full Model: {model_full.rsquared:.4f}")
    print(f"AIC Full Model: {model_full.aic:.2f}")
    
    # === STEPWISE SELECTION SIMULATION ===
    print("\n" + "="*80)
    print("2. SIMULASI STEPWISE SELECTION")
    print("-" * 50)
    
    # Start with only significant teams (p < 0.05)
    significant_teams = [result['team'] for result in significance_results if result['significant']]
    
    print("Tim yang SIGNIFIKAN (p < 0.05):")
    for result in significance_results:
        if result['significant']:
            print(f"  ✓ {result['team']:<15} p = {result['p_value']:.4f}")
    
    print("\nTim yang TIDAK SIGNIFIKAN (p ≥ 0.05):")
    for result in significance_results:
        if not result['significant']:
            print(f"  ✗ {result['team']:<15} p = {result['p_value']:.4f}")
    
    # === MODEL 2: STEPWISE MODEL (HANYA TIM SIGNIFIKAN) ===
    print("\n" + "="*80)
    print("3. STEPWISE MODEL (HANYA TIM SIGNIFIKAN)")
    print("-" * 50)
    
    # Filter team dummies for significant teams only
    team_dummies_significant = team_dummies[significant_teams]
    
    X_stepwise = pd.concat([df[['driverorder2']], team_dummies_significant], axis=1)
    X_stepwise = sm.add_constant(X_stepwise)
    
    model_stepwise = sm.OLS(y, X_stepwise).fit()
    
    print("Hasil Model Stepwise:")
    print(f"{'Variabel':<15} {'Coefficient':<12} {'Std Error':<12} {'t-value':<10} {'p-value':<12}")
    print("-" * 75)
    
    for var in model_stepwise.params.index:
        if var == 'const':
            var_display = '(Intercept)'
        elif var == 'driverorder2':
            var_display = 'Second driver'
        else:
            var_display = var
            
        coef = model_stepwise.params[var]
        stderr = model_stepwise.bse[var]
        t_val = model_stepwise.tvalues[var]
        p_val = model_stepwise.pvalues[var]
        
        print(f"{var_display:<15} {coef:<12.4f} {stderr:<12.4f} {t_val:<10.3f} {p_val:<12.4f}")
    
    print(f"\nR² Stepwise Model: {model_stepwise.rsquared:.4f}")
    print(f"AIC Stepwise Model: {model_stepwise.aic:.2f}")
    
    # === COMPARISON WITH JOURNAL ===
    print("\n" + "="*80)
    print("4. PERBANDINGAN DENGAN JURNAL")
    print("-" * 50)
    
    journal_r2 = 0.3914
    journal_teams = ['RedBull', 'Mercedes', 'Ferrari', 'Mclaren', 'Alpine', 'AstonMartin']
    
    print(f"Jurnal R²: {journal_r2}")
    print(f"Stepwise R²: {model_stepwise.rsquared:.4f}")
    print(f"Full R²: {model_full.rsquared:.4f}")
    print()
    print(f"Tim dalam jurnal: {len(journal_teams)} tim")
    print(f"Tim stepwise: {len(significant_teams)} tim")
    print()
    print("Apakah tim stepwise = tim jurnal?", set(significant_teams) == set(journal_teams))
    
    # === MENGAPA STEPWISE? ===
    print("\n" + "="*80)
    print("5. MENGAPA STEPWISE REGRESSION?")
    print("-" * 50)
    
    print("KEUNTUNGAN STEPWISE:")
    print("✓ Menghindari overfitting")
    print("✓ Model lebih sederhana dan interpretable")
    print("✓ Menghilangkan variabel yang tidak berkontribusi signifikan")
    print("✓ AIC yang lebih baik (lower is better)")
    print("✓ Generalizable ke data baru")
    
    print("\nKERUGIAN FULL MODEL:")
    print("✗ Overfitting (R² tinggi tapi tidak generalizable)")
    print("✗ Multicollinearity antar variabel")
    print("✗ Interpretasi lebih sulit")
    print("✗ AIC yang lebih buruk")
    
    aic_difference = model_full.aic - model_stepwise.aic
    print(f"\nPerbedaan AIC: {aic_difference:.2f}")
    print("(AIC lebih rendah = model lebih baik)")
    
    return model_full, model_stepwise

if __name__ == "__main__":
    analyze_statistical_significance()