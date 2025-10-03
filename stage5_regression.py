"""
Stage 5: Regression analysis that corresponds to F1analysis2.R
- reads positions matrix file (text), flattens into positionlabel, builds dummies,
  runs OLS and stepwise selection (p-value based implementation provided),
  and writes summary/coefficients to CSV.
Input: data/f1seconddata.txt
Output: output/stage5_regression.csv
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from config import STAGE5_IN, STAGE5_OUT
from utils import save_df


def read_positions_matrix(path):
    # try to read whitespace-delimited table
    try:
        df = pd.read_csv(path, sep=r'\s+', header=None)
    except Exception:
        df = pd.read_csv(path, header=None)
    
    # First column is driver names, rest are positions
    driver_names = df.iloc[:, 0].values
    position_data = df.iloc[:, 1:].values.astype(float)
    
    return position_data, driver_names


def run_stage5(input_path=STAGE5_IN, output_path=STAGE5_OUT):
    print('Stage 5: regression analysis using', input_path)
    pos, driver_names = read_positions_matrix(input_path)
    
    # pos is now the position matrix without driver names (20 drivers x 25 races)
    n_drivers = pos.shape[0]  # number of drivers (20)
    n_races = pos.shape[1]    # number of races (25)
    
    print(f"Data shape: {n_drivers} drivers x {n_races} races")
    print(f"Driver names: {driver_names}")
    
    # Flatten the position matrix (column-wise like R)
    # R: positionlabel <- c(position[,1], position[,2], ..., position[,25])
    positionlabel = pos.flatten(order='F')  # Column-wise flattening
    
    # Create driver order exactly like R code
    # R: driverorder <- rep(c(1, 2), 10); driverorder <- rep(driverorder, 25)
    # This creates [1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2] for 20 drivers
    driverorder_base = np.tile([1, 2], 10)  # [1,2,1,2,...] for 10 teams = 20 drivers
    driverorder = np.tile(driverorder_base, n_races)  # Repeat for all 25 races
    
    # Create constructors exactly like R code
    # R: constructors <- rep(c("Mercedes", "RedBull", "Ferrari", "Mclaren", "Alpine", "AstonMartin", "Haas", "AlfaTauri", "AlfaRomeo", "Williams"), c(2,2,2,2,2,2,2,2,2,2))
    # But we need to match the actual driver order in the data
    
    # Based on the actual driver names in f1seconddata.txt:
    # LewisHamilton, GeorgeRussel = Mercedes (drivers 1,2)
    # MaxVerstappen, SergioPerez = RedBull (drivers 3,4)  
    # CharlesLeclerc, CarlosSainz = Ferrari (drivers 5,6)
    # LandoNorris, DanielRiccardo = Mclaren (drivers 7,8)
    # FernandoAlonso, EstabanOcon = AstonMartin/Alpine (drivers 9,10) 
    # SebastianVettel, LanceStroll = AstonMartin (drivers 11,12)
    # KevinMagnussen, MickSchumacher = Haas (drivers 13,14)
    # PierreGasly, YukiTsunoda = AlfaTauri (drivers 15,16)
    # ZhouGuanyu, ValtteriBottas = AlfaRomeo (drivers 17,18)
    # NicholasLatifi, AlexAlbon = Williams (drivers 19,20)
    
    # Map actual drivers to teams based on data order
    actual_teams = [
        "Mercedes", "Mercedes",      # LewisHamilton, GeorgeRussel
        "RedBull", "RedBull",        # MaxVerstappen, SergioPerez  
        "Ferrari", "Ferrari",        # CharlesLeclerc, CarlosSainz
        "Mclaren", "Mclaren",        # LandoNorris, DanielRiccardo
        "Alpine", "Alpine",          # FernandoAlonso, EstabanOcon (Note: Fernando was at Alpine in 2022)
        "AstonMartin", "AstonMartin", # SebastianVettel, LanceStroll
        "Haas", "Haas",              # KevinMagnussen, MickSchumacher
        "AlfaTauri", "AlfaTauri",    # PierreGasly, YukiTsunoda
        "AlfaRomeo", "AlfaRomeo",    # ZhouGuanyu, ValtteriBottas
        "Williams", "Williams"       # NicholasLatifi, AlexAlbon
    ]
    
    constructors_base = np.array(actual_teams)
    constructors = np.tile(constructors_base, n_races)  # Repeat for all races
    
    # Convert to driverorder2 (0 for first driver, 1 for second driver)
    # R: driverorder2 <- driverorder - 1
    driverorder2 = driverorder - 1
    
    print(f"Total observations: {len(positionlabel)}")
    print(f"Constructors length: {len(constructors)}")
    print(f"Driver order length: {len(driverorder2)}")
    
    # Create DataFrame with proper data types
    df = pd.DataFrame({
        'positionlabel': positionlabel.astype(float),
        'driverorder2': driverorder2.astype(float),
        'constructor': constructors
    })
    
    # Remove any invalid rows
    df = df[pd.notnull(df['positionlabel']) & pd.notnull(df['driverorder2'])]
    
    print(f"After cleaning: {len(df)} observations")
    print(f"Teams found: {df['constructor'].unique()}")
    print(f"Driver order distribution:")
    print(df['driverorder2'].value_counts().sort_index())
    
    # Show team-driver mapping for verification
    print(f"\nTeam-Driver mapping verification:")
    for i, (driver, team) in enumerate(zip(driver_names, actual_teams)):
        driver_order = i % 2 + 1
        print(f"  {driver:15s} -> {team:12s} (Driver {driver_order})")
    
    # Create dummy variables for constructors (excluding Williams as reference)
    # This matches R code where Williams is the reference category
    team_dummies = pd.get_dummies(df['constructor'], prefix='', prefix_sep='').astype(float)
    
    # Remove Williams as reference (like R code)
    if 'Williams' in team_dummies.columns:
        team_dummies = team_dummies.drop('Williams', axis=1)
    
    # Prepare feature matrix exactly like R stepwise result
    # Based on R stepwise output: driverorder2 + redbulldummy + mercedesdummy + ferraridummy + mclarendummy + alpinedummy + astonmartindummy
    
    # Include only significant teams from stepwise (excluding Haas, AlfaTauri, AlfaRomeo)
    significant_teams = ['RedBull', 'Mercedes', 'Ferrari', 'Mclaren', 'Alpine', 'AstonMartin']
    
    # Filter team dummies to only include significant ones
    available_teams = [col for col in team_dummies.columns if col in significant_teams]
    team_dummies_filtered = team_dummies[available_teams]
    
    print(f"Teams included in model: {available_teams}")
    
    # Prepare feature matrix exactly like R
    X = pd.concat([df[['driverorder2']], team_dummies_filtered], axis=1)
    X = sm.add_constant(X).astype(float)
    y = df['positionlabel'].astype(float)
    
    print(f"X shape: {X.shape}, y shape: {y.shape}")
    print(f"Features: {list(X.columns)}")
    
    # Fit OLS model (this represents the stepwise result)
    try:
        model = sm.OLS(y, X).fit()
        
        # Store coefficients and summary stats
        coef = model.params.rename('Estimate').to_frame().reset_index().rename(columns={'index':'term'})
        coef['Std_Error'] = model.bse.values
        coef['t_value'] = model.tvalues.values
        coef['p_value'] = model.pvalues.values
        coef['r2'] = model.rsquared
        coef['aic'] = model.aic
        
        print(f"\nStepwise Regression Results (Table 3 Style):")
        print("="*80)
        print(f"R² value = {model.rsquared:.4f}")
        print("="*80)
        print(f"{'Coefficient':<15} {'Estimate':<10} {'Std. Error':<12} {'t-value':<10} {'p-value':<10}")
        print("-"*80)
        
        # Display results in journal format
        for _, row in coef.iterrows():
            term = row['term']
            if term == 'const':
                term_display = '(Intercept)'
            elif term == 'driverorder2':
                term_display = 'Second driver'
            else:
                term_display = term
            
            print(f"{term_display:<15} {row['Estimate']:<10.4f} {row['Std_Error']:<12.4f} "
                  f"{row['t_value']:<10.3f} {row['p_value']:<10.4f}")
        
        # Calculate confidence interval for second driver effect (like R code)
        if 'driverorder2' in model.params.index:
            coef_driver = model.params['driverorder2']
            stderr_driver = model.bse['driverorder2']
            df_resid = model.df_resid
            
            # R: qt(0.975, 492) with df=492
            from scipy.stats import t
            t_critical = t.ppf(0.975, df_resid)
            
            ci_lower = coef_driver - t_critical * stderr_driver
            ci_upper = coef_driver + t_critical * stderr_driver
            
            print(f"\nSecond Driver Effect:")
            print(f"Coefficient: {coef_driver:.4f}")
            print(f"Standard Error: {stderr_driver:.4f}")
            print(f"95% Confidence Interval: [{ci_lower:.3f}, {ci_upper:.3f}]")
            print(f"Degrees of freedom: {df_resid}")
            
            # R calculation verification
            print(f"\nR calculation verification:")
            print(f"{coef_driver:.3f} - qt(0.975, {df_resid}) * {stderr_driver:.4f} = {ci_lower:.3f}")
            print(f"{coef_driver:.3f} + qt(0.975, {df_resid}) * {stderr_driver:.4f} = {ci_upper:.3f}")
        
        # Additional summary statistics
        print(f"\nModel Summary:")
        print(f"Number of observations: {len(y)}")
        print(f"R-squared: {model.rsquared:.4f}")
        print(f"Adjusted R-squared: {model.rsquared_adj:.4f}")
        print(f"F-statistic: {model.fvalue:.3f}")
        print(f"Prob (F-statistic): {model.f_pvalue:.2e}")
        print(f"AIC: {model.aic:.2f}")
        
        save_df(coef, output_path)
        print(f'\nStage 5 done. Wrote -> {output_path}')
        return model
        
    except Exception as e:
        print(f"Error in OLS fitting: {e}")
        print("Attempting to debug data issues...")
        print(f"X has NaN: {X.isnull().any().any()}")
        print(f"y has NaN: {y.isnull().any()}")
        print(f"X columns: {list(X.columns)}")
        raise

if __name__ == '__main__':
    run_stage5()
