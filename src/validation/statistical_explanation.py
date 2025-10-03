"""
PENJELASAN MENDALAM: TIM SIGNIFIKAN SECARA STATISTIK
"""

print("="*80)
print("PENJELASAN LENGKAP: STEPWISE REGRESSION DALAM F1 ANALYSIS")
print("="*80)

print("\n1. PARAMETER SIGNIFIKANSI STATISTIK")
print("-" * 50)
print("• P-VALUE: Probabilitas mendapatkan hasil ini jika tidak ada efek nyata")
print("  - p < 0.001: Sangat signifikan (***)")
print("  - p < 0.01:  Signifikan (**)")
print("  - p < 0.05:  Cukup signifikan (*)")
print("  - p ≥ 0.05:  Tidak signifikan")
print()
print("• T-STATISTIC: coefficient / standard_error")
print("  - |t| > 1.96: Signifikan pada α = 0.05")
print("  - |t| > 2.58: Signifikan pada α = 0.01")
print("  - Semakin besar |t|, semakin kuat efeknya")

print("\n2. HASIL ANALISIS KITA VS JURNAL")
print("-" * 50)

# Data dari analisis
teams_analysis = {
    'RedBull': {'p': 0.0000, 't': -12.242, 'coef': -11.0600, 'in_journal': True},
    'Mercedes': {'p': 0.0000, 't': -10.715, 'coef': -9.6800, 'in_journal': True},
    'Ferrari': {'p': 0.0000, 't': -10.073, 'coef': -9.1000, 'in_journal': True},
    'Mclaren': {'p': 0.0000, 't': -5.490, 'coef': -4.9600, 'in_journal': True},
    'Alpine': {'p': 0.0000, 't': -5.490, 'coef': -4.9600, 'in_journal': True},
    'AstonMartin': {'p': 0.0004, 't': -3.542, 'coef': -3.2000, 'in_journal': True},
    'AlfaRomeo': {'p': 0.0162, 't': -2.413, 'coef': -2.1800, 'in_journal': False},
    'AlfaTauri': {'p': 0.0547, 't': -1.926, 'coef': -1.7400, 'in_journal': False},
    'Haas': {'p': 0.0575, 't': -1.904, 'coef': -1.7200, 'in_journal': False}
}

print(f"{'Tim':<12} {'P-value':<10} {'t-value':<10} {'Coefficient':<12} {'Jurnal?':<8} {'Alasan'}")
print("-" * 75)

for team, data in teams_analysis.items():
    journal_status = "YA" if data['in_journal'] else "TIDAK"
    
    if data['p'] < 0.001:
        reason = "Sangat signifikan"
    elif data['p'] < 0.01:
        reason = "Signifikan"
    elif data['p'] < 0.05:
        reason = "Marginal"
    else:
        reason = "Tidak signifikan"
    
    print(f"{team:<12} {data['p']:<10.4f} {data['t']:<10.3f} {data['coef']:<12.4f} {journal_status:<8} {reason}")

print("\n3. MENGAPA JURNAL EXCLUDE AlfaRomeo?")
print("-" * 50)
print("Meskipun AlfaRomeo signifikan (p = 0.0162 < 0.05), jurnal mungkin:")
print("• Menggunakan threshold yang lebih ketat (p < 0.01)")
print("• Menerapkan Bonferroni correction untuk multiple testing")
print("• Menggunakan stepwise backward elimination dengan AIC/BIC criteria")
print("• Mempertimbangkan practical significance, bukan hanya statistical significance")

print("\n4. JENIS-JENIS STEPWISE REGRESSION")
print("-" * 50)
print("• FORWARD SELECTION:")
print("  - Mulai tanpa variabel, tambah satu per satu")
print("  - Kriteria: p-to-enter < 0.05")
print()
print("• BACKWARD ELIMINATION:")
print("  - Mulai dengan semua variabel, buang satu per satu")
print("  - Kriteria: p-to-remove > 0.10")
print()
print("• BIDIRECTIONAL (STEPWISE):")
print("  - Kombinasi forward dan backward")
print("  - Bisa menambah dan membuang variabel")

print("\n5. KRITERIA SELEKSI VARIABEL")
print("-" * 50)
print("• STATISTICAL SIGNIFICANCE:")
print("  - P-value threshold (biasanya 0.05)")
print("  - F-statistic untuk overall model")
print()
print("• INFORMATION CRITERIA:")
print("  - AIC (Akaike Information Criterion) - lower is better")
print("  - BIC (Bayesian Information Criterion)")
print("  - Penalizes model complexity")
print()
print("• PRACTICAL CONSIDERATIONS:")
print("  - Effect size (besar efek)")
print("  - Multicollinearity (VIF < 10)")
print("  - Domain knowledge")

print("\n6. MENGAPA HANYA TIM SIGNIFIKAN?")
print("-" * 50)
print("✓ BIAS REDUCTION: Mencegah overfitting pada data training")
print("✓ INTERPRETABILITY: Model lebih mudah dijelaskan")
print("✓ EFFICIENCY: Fokus pada faktor yang benar-benar berpengaruh")
print("✓ GENERALIZABILITY: Performa lebih baik pada data baru")
print("✓ STATISTICAL POWER: Konsentrasi pada efek yang robust")

print("\n7. CONTOH KONKRET DARI HASIL:")
print("-" * 50)
print("• RedBull (p < 0.001): Efek sangat kuat dan konsisten")
print("  → 99.9% yakin bahwa RedBull berbeda dari Williams")
print()
print("• AlfaRomeo (p = 0.016): Efek marginal")
print("  → 98.4% yakin, tapi mungkin tidak robust di data lain")
print()
print("• Haas (p = 0.058): Tidak signifikan")
print("  → Hanya 94.2% yakin, terlalu besar kemungkinan kebetulan")

print("\n8. IMPLIKASI PRAKTIS:")
print("-" * 50)
print("Dalam konteks F1:")
print("• Tim signifikan = Tim yang KONSISTEN berbeda performa dari baseline")
print("• Tim tidak signifikan = Performa tidak berbeda secara meaningful")
print("• Baseline (Williams) = Tim referensi untuk perbandingan")
print()
print("Jadi stepwise membantu mengidentifikasi tim mana yang")
print("BENAR-BENAR memiliki keunggulan/kelemahan yang dapat diandalkan")
print("vs tim yang performanya mungkin hanya kebetulan.")

print("\n" + "="*80)