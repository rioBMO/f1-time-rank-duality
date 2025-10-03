"""
SIMULASI MONTE CARLO UNTUK VALIDASI MODEL DISTRIBUSI EXPONENTIAL
================================================================

Tujuan: Memberikan bukti empiris bahwa hasil perhitungan teoritis dari model
distribusi exponential sesuai dengan simulasi Monte Carlo.

Model Teoritis:
- Waktu lap mengikuti distribusi exponential dengan parameter lambda
- P(posisi = k) = probabilitas driver berada di posisi ke-k
- Estimasi lambda menggunakan maximum likelihood (grouped approach)
- Hubungan: mu = -log(p_norm), sigma = sqrt(trigamma(1))
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import gamma, digamma, polygamma
from stage2_probabilities import run_stage2
from stage3_estimate_lambda import run_stage3
from stage4_mu_sigma import run_stage4
import warnings
warnings.filterwarnings('ignore')

class MonteCarloF1Simulator:
    """
    Simulator Monte Carlo untuk model F1 dengan distribusi exponential
    """
    
    def __init__(self, n_simulations=10000, n_drivers=20, n_races=25):
        self.n_simulations = n_simulations
        self.n_drivers = n_drivers
        self.n_races = n_races
        self.results = {}
        
    def load_theoretical_parameters(self):
        """Load parameter teoritis dari hasil stage 2-4"""
        print("Loading theoretical parameters from pipeline...")
        
        # Load normalized probabilities (stage 2)
        prob_df = pd.read_csv('output/stage2_probabilities.csv')
        self.p_norm_theoretical = prob_df['p_norm'].values
        self.driver_names = prob_df['Driver'].values
        
        # Load lambda estimates (stage 3) 
        lambda_df = pd.read_csv('output/stage3_lambda.csv')
        self.lambda_theoretical = lambda_df['lambda_est'].values
        
        # Load mu and sigma (stage 4)
        mu_sigma_df = pd.read_csv('output/stage4_mu_sigma.csv')
        self.mu_theoretical = mu_sigma_df['mu_hat'].values
        self.sigma_theoretical = mu_sigma_df['sigma_hat'].values
        
        print(f"Loaded {len(self.p_norm_theoretical)} drivers parameters")
        
    def simulate_exponential_times(self, lambda_params):
        """
        Simulasi waktu lap menggunakan distribusi exponential
        
        Args:
            lambda_params: array parameter lambda untuk setiap driver
            
        Returns:
            simulated_times: matrix (n_drivers x n_races x n_simulations)
        """
        simulated_times = np.zeros((self.n_drivers, self.n_races, self.n_simulations))
        
        for sim in range(self.n_simulations):
            for driver_idx in range(self.n_drivers):
                # Generate exponential random times for each race
                times = np.random.exponential(1/lambda_params[driver_idx], self.n_races)
                simulated_times[driver_idx, :, sim] = times
                
        return simulated_times
    
    def times_to_positions(self, times):
        """
        Konversi waktu lap ke posisi (ranking)
        
        Args:
            times: array waktu lap (n_drivers x n_races)
            
        Returns:
            positions: array posisi (n_drivers x n_races)
        """
        positions = np.zeros_like(times, dtype=int)
        
        for race in range(self.n_races):
            race_times = times[:, race]
            # Sort and get positions (1 = fastest, 20 = slowest)
            sorted_indices = np.argsort(race_times)
            positions[sorted_indices, race] = np.arange(1, self.n_drivers + 1)
            
        return positions
    
    def calculate_empirical_probabilities(self, positions):
        """
        Hitung probabilitas empiris dari simulasi
        
        Args:
            positions: array posisi (n_drivers x n_races x n_simulations)
            
        Returns:
            empirical_probs: probabilitas setiap driver menang
        """
        # Count wins (position = 1) for each driver across all simulations and races
        wins = np.sum(positions == 1, axis=(1, 2))  # Sum over races and simulations
        total_opportunities = self.n_races * self.n_simulations
        
        empirical_probs = wins / total_opportunities
        return empirical_probs
    
    def run_monte_carlo_validation(self):
        """
        Jalankan validasi Monte Carlo lengkap
        """
        print("="*80)
        print("SIMULASI MONTE CARLO UNTUK VALIDASI MODEL F1")
        print("="*80)
        print(f"Jumlah simulasi: {self.n_simulations:,}")
        print(f"Jumlah driver: {self.n_drivers}")
        print(f"Jumlah race: {self.n_races}")
        print()
        
        # 1. Load theoretical parameters
        self.load_theoretical_parameters()
        
        # 2. Run Monte Carlo simulation
        print("Running Monte Carlo simulations...")
        simulated_times = self.simulate_exponential_times(self.lambda_theoretical)
        
        # 3. Convert times to positions for each simulation
        print("Converting times to positions...")
        all_positions = np.zeros((self.n_drivers, self.n_races, self.n_simulations))
        
        for sim in range(self.n_simulations):
            if (sim + 1) % 1000 == 0:
                print(f"  Processing simulation {sim + 1:,}/{self.n_simulations:,}")
            all_positions[:, :, sim] = self.times_to_positions(simulated_times[:, :, sim])
        
        # 4. Calculate empirical probabilities
        print("Calculating empirical probabilities...")
        empirical_probs = self.calculate_empirical_probabilities(all_positions)
        
        # 5. Compare with theoretical
        self.compare_theoretical_vs_empirical(empirical_probs)
        
        # 6. Statistical tests
        self.run_statistical_tests(empirical_probs)
        
        # 7. Detailed analysis for top drivers
        self.detailed_driver_analysis(all_positions)
        
        # 8. Generate plots
        self.generate_validation_plots(empirical_probs)
        
        return empirical_probs
    
    def compare_theoretical_vs_empirical(self, empirical_probs):
        """
        Bandingkan probabilitas teoritis vs empiris
        """
        print("\n" + "="*80)
        print("PERBANDINGAN PROBABILITAS TEORITIS VS EMPIRIS")
        print("="*80)
        
        # Sort by theoretical probability (descending)
        sorted_indices = np.argsort(self.p_norm_theoretical)[::-1]
        
        print(f"{'Driver':<15} {'Theoretical':<12} {'Empirical':<12} {'Difference':<12} {'Rel Error %':<12}")
        print("-" * 75)
        
        total_abs_error = 0
        total_rel_error = 0
        
        for i in sorted_indices[:10]:  # Top 10 drivers
            driver = self.driver_names[i]
            theoretical = self.p_norm_theoretical[i]
            empirical = empirical_probs[i]
            difference = empirical - theoretical
            rel_error = abs(difference / theoretical) * 100 if theoretical > 0 else 0
            
            total_abs_error += abs(difference)
            total_rel_error += rel_error
            
            print(f"{driver:<15} {theoretical:<12.6f} {empirical:<12.6f} "
                  f"{difference:<12.6f} {rel_error:<12.2f}")
        
        print("-" * 75)
        print(f"{'Average':<15} {'':<12} {'':<12} "
              f"{total_abs_error/10:<12.6f} {total_rel_error/10:<12.2f}")
        
        # Overall correlation
        correlation = np.corrcoef(self.p_norm_theoretical, empirical_probs)[0, 1]
        print(f"\nCorrelation coefficient: {correlation:.6f}")
        
        # R-squared
        r_squared = correlation ** 2
        print(f"R-squared: {r_squared:.6f}")
        
        # Mean Absolute Error
        mae = np.mean(np.abs(empirical_probs - self.p_norm_theoretical))
        print(f"Mean Absolute Error: {mae:.8f}")
        
        # Root Mean Square Error
        rmse = np.sqrt(np.mean((empirical_probs - self.p_norm_theoretical) ** 2))
        print(f"Root Mean Square Error: {rmse:.8f}")
        
    def run_statistical_tests(self, empirical_probs):
        """
        Jalankan tes statistik untuk validasi
        """
        print("\n" + "="*80)
        print("TES STATISTIK VALIDASI")
        print("="*80)
        
        # 1. Kolmogorov-Smirnov test
        ks_stat, ks_pvalue = stats.ks_2samp(self.p_norm_theoretical, empirical_probs)
        print(f"Kolmogorov-Smirnov Test:")
        print(f"  Statistic: {ks_stat:.6f}")
        print(f"  P-value: {ks_pvalue:.6f}")
        print(f"  Result: {'PASS' if ks_pvalue > 0.05 else 'FAIL'} (α = 0.05)")
        
        # 2. Wilcoxon signed-rank test
        wilcoxon_stat, wilcoxon_pvalue = stats.wilcoxon(
            self.p_norm_theoretical, empirical_probs, alternative='two-sided'
        )
        print(f"\nWilcoxon Signed-Rank Test:")
        print(f"  Statistic: {wilcoxon_stat:.6f}")
        print(f"  P-value: {wilcoxon_pvalue:.6f}")
        print(f"  Result: {'PASS' if wilcoxon_pvalue > 0.05 else 'FAIL'} (α = 0.05)")
        
        # 3. Paired t-test
        t_stat, t_pvalue = stats.ttest_rel(self.p_norm_theoretical, empirical_probs)
        print(f"\nPaired T-Test:")
        print(f"  Statistic: {t_stat:.6f}")
        print(f"  P-value: {t_pvalue:.6f}")
        print(f"  Result: {'PASS' if t_pvalue > 0.05 else 'FAIL'} (α = 0.05)")
        
        # 4. Check if differences are within Monte Carlo error bounds
        # Standard error for binomial proportion: sqrt(p(1-p)/n)
        print(f"\nMonte Carlo Error Analysis:")
        total_trials = self.n_races * self.n_simulations
        
        within_bounds = 0
        for i in range(len(empirical_probs)):
            p = self.p_norm_theoretical[i]
            se = np.sqrt(p * (1 - p) / total_trials)
            margin_error = 1.96 * se  # 95% confidence interval
            
            lower_bound = p - margin_error
            upper_bound = p + margin_error
            
            if lower_bound <= empirical_probs[i] <= upper_bound:
                within_bounds += 1
        
        pct_within_bounds = (within_bounds / len(empirical_probs)) * 100
        print(f"  Drivers within 95% CI: {within_bounds}/{len(empirical_probs)} ({pct_within_bounds:.1f}%)")
        print(f"  Expected: ~95% for valid model")
        
    def detailed_driver_analysis(self, all_positions):
        """
        Analisis detail untuk driver teratas
        """
        print("\n" + "="*80)
        print("ANALISIS DETAIL DRIVER TERATAS")
        print("="*80)
        
        # Focus on top 5 drivers by theoretical probability
        top_indices = np.argsort(self.p_norm_theoretical)[::-1][:5]
        
        for idx in top_indices:
            driver = self.driver_names[idx]
            theoretical_p = self.p_norm_theoretical[idx]
            lambda_param = self.lambda_theoretical[idx]
            
            print(f"\n{driver} Analysis:")
            print(f"  Theoretical win probability: {theoretical_p:.6f}")
            print(f"  Lambda parameter: {lambda_param:.6f}")
            
            # Calculate position distribution from simulations
            driver_positions = all_positions[idx, :, :].flatten().astype(int)  # All positions across races and sims
            
            position_counts = np.bincount(driver_positions, minlength=21)[1:21]  # Positions 1-20
            position_probs = position_counts / len(driver_positions)
            
            print(f"  Empirical position distribution:")
            for pos in range(1, 6):  # Top 5 positions
                print(f"    P(position = {pos}): {position_probs[pos-1]:.6f}")
            
            # Expected vs actual wins
            expected_wins = theoretical_p * self.n_races * self.n_simulations
            actual_wins = np.sum(driver_positions == 1)
            print(f"  Expected wins: {expected_wins:.1f}")
            print(f"  Actual wins: {actual_wins}")
            print(f"  Win rate: {actual_wins / (self.n_races * self.n_simulations):.6f}")
    
    def generate_validation_plots(self, empirical_probs):
        """
        Generate plots untuk validasi visual
        """
        print("\n" + "="*80)
        print("GENERATING VALIDATION PLOTS")
        print("="*80)
        
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Monte Carlo Validation of F1 Exponential Model', fontsize=16, fontweight='bold')
        
        # Plot 1: Theoretical vs Empirical scatter
        ax1 = axes[0, 0]
        ax1.scatter(self.p_norm_theoretical, empirical_probs, alpha=0.7, s=60)
        
        # Perfect correlation line
        min_val = min(min(self.p_norm_theoretical), min(empirical_probs))
        max_val = max(max(self.p_norm_theoretical), max(empirical_probs))
        ax1.plot([min_val, max_val], [min_val, max_val], 'r--', label='Perfect correlation')
        
        ax1.set_xlabel('Theoretical Probability')
        ax1.set_ylabel('Empirical Probability')
        ax1.set_title('Theoretical vs Empirical Probabilities')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Add correlation coefficient
        correlation = np.corrcoef(self.p_norm_theoretical, empirical_probs)[0, 1]
        ax1.text(0.05, 0.95, f'r = {correlation:.4f}', transform=ax1.transAxes, 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Plot 2: Residuals
        ax2 = axes[0, 1]
        residuals = empirical_probs - self.p_norm_theoretical
        ax2.scatter(self.p_norm_theoretical, residuals, alpha=0.7, s=60)
        ax2.axhline(y=0, color='r', linestyle='--')
        ax2.set_xlabel('Theoretical Probability')
        ax2.set_ylabel('Residuals (Empirical - Theoretical)')
        ax2.set_title('Residual Plot')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Distribution comparison for top drivers
        ax3 = axes[1, 0]
        top_5_indices = np.argsort(self.p_norm_theoretical)[::-1][:5]
        
        x_pos = np.arange(len(top_5_indices))
        width = 0.35
        
        theoretical_top5 = self.p_norm_theoretical[top_5_indices]
        empirical_top5 = empirical_probs[top_5_indices]
        
        ax3.bar(x_pos - width/2, theoretical_top5, width, label='Theoretical', alpha=0.8)
        ax3.bar(x_pos + width/2, empirical_top5, width, label='Empirical', alpha=0.8)
        
        ax3.set_xlabel('Top 5 Drivers')
        ax3.set_ylabel('Win Probability')
        ax3.set_title('Top 5 Drivers: Theoretical vs Empirical')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels([self.driver_names[i][:8] for i in top_5_indices], rotation=45)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Error distribution
        ax4 = axes[1, 1]
        errors = empirical_probs - self.p_norm_theoretical
        ax4.hist(errors, bins=15, alpha=0.7, edgecolor='black')
        ax4.axvline(x=0, color='r', linestyle='--', label='Zero error')
        ax4.set_xlabel('Error (Empirical - Theoretical)')
        ax4.set_ylabel('Frequency')
        ax4.set_title('Distribution of Errors')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Add statistics
        mean_error = np.mean(errors)
        std_error = np.std(errors)
        ax4.text(0.05, 0.95, f'Mean: {mean_error:.6f}\nStd: {std_error:.6f}', 
                transform=ax4.transAxes, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('output/monte_carlo_validation.png', dpi=300, bbox_inches='tight')
        print("Saved validation plots to output/monte_carlo_validation.png")
        
        # Show plot if running interactively
        try:
            plt.show()
        except:
            pass
    
    def generate_summary_report(self, empirical_probs):
        """
        Generate ringkasan laporan validasi
        """
        correlation = np.corrcoef(self.p_norm_theoretical, empirical_probs)[0, 1]
        mae = np.mean(np.abs(empirical_probs - self.p_norm_theoretical))
        rmse = np.sqrt(np.mean((empirical_probs - self.p_norm_theoretical) ** 2))
        
        report = f"""
MONTE CARLO VALIDATION REPORT
============================

Model: Exponential Distribution for F1 Lap Times
Simulations: {self.n_simulations:,}
Drivers: {self.n_drivers}
Races: {self.n_races}

VALIDATION METRICS:
- Correlation: {correlation:.6f}
- R-squared: {correlation**2:.6f}
- Mean Absolute Error: {mae:.8f}
- Root Mean Square Error: {rmse:.8f}

CONCLUSION:
{'VALID: Model confirmed by Monte Carlo simulation' if correlation > 0.99 else 'INVALID: Significant discrepancy found'}

The exponential distribution model for F1 lap times is {'well-supported' if correlation > 0.99 else 'questionable'} by empirical evidence.
Monte Carlo simulation with {self.n_simulations:,} iterations shows {'excellent' if correlation > 0.99 else 'poor'} agreement with theoretical predictions.
"""
        
        # Save report
        with open('output/monte_carlo_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n" + "="*80)
        print("SUMMARY REPORT")
        print("="*80)
        print(report)
        print(f"Full report saved to output/monte_carlo_report.txt")


def main():
    """
    Main function untuk menjalankan simulasi Monte Carlo
    """
    print("MONTE CARLO SIMULATION FOR F1 EXPONENTIAL MODEL VALIDATION")
    print("=" * 80)
    
    # Ensure we have the theoretical results first
    print("1. Generating theoretical results (if needed)...")
    try:
        # Check if files exist, if not run the pipeline
        import os
        if not all(os.path.exists(f'output/stage{i}_{name}.csv') for i, name in 
                  [(2, 'probabilities'), (3, 'lambda'), (4, 'mu_sigma')]):
            print("   Running stages 2-4 to generate theoretical parameters...")
            run_stage2()
            run_stage3()  
            run_stage4()
    except Exception as e:
        print(f"   Error running pipeline: {e}")
        return
    
    # Create and run Monte Carlo simulator
    print("\n2. Initializing Monte Carlo simulator...")
    simulator = MonteCarloF1Simulator(
        n_simulations=10000,  # Adjust based on computational resources
        n_drivers=20,
        n_races=25
    )
    
    print("\n3. Running Monte Carlo validation...")
    empirical_probs = simulator.run_monte_carlo_validation()
    
    print("\n4. Generating summary report...")
    simulator.generate_summary_report(empirical_probs)
    
    print("\n" + "="*80)
    print("MONTE CARLO VALIDATION COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("Check the following output files:")
    print("- output/monte_carlo_validation.png (validation plots)")
    print("- output/monte_carlo_report.txt (summary report)")


if __name__ == "__main__":
    main()