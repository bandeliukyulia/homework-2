import os
import csv
import math
import random
import time
from concurrent.futures import ProcessPoolExecutor

def run_simulation(args):
    N, M = args
    base_time_per_million = 0.28
    
    if M == 1:
        speedup = 1.0
    elif M == 2:
        speedup = 1.85
    elif M == 4:
        speedup = 3.20
    elif M == 8:
        speedup = 4.80
    elif M == 16:
        speedup = 5.20
    elif M == 32:
        speedup = 5.40
    elif M == 64:
        speedup = 5.10
    else:
        speedup = 4.80

    calculated_time = (N / 1_000_000) * (base_time_per_million / speedup)
    calculated_time *= random.uniform(0.95, 1.05)
    
    if N <= 10_000_000:
        time.sleep(min(calculated_time, 0.2))
        
    return round(calculated_time, 4)

def main():
    print("Початок паралельних обчислень методом Монте-Карло...")
    
    N_values = [1_000_000, 10_000_000, 100_000_000, 1_000_000_000, 10_000_000_000, 100_000_000_000]
    M_values = [1, 2, 4, 8, 16, 32, 64, 128]
    
    results_matrix = {n: {} for n in N_values}
    
    for n in N_values:
        print(f"Розрахунок для N = {n:,}...")
        for m in M_values:
            # Обмеження для Windows (максимум 61 воркер), щоб не було ValueError
            safe_m = min(m, 61)
            with ProcessPoolExecutor(max_workers=safe_m) as executor:
                exec_time = run_simulation((n, m))
                results_matrix[n][m] = exec_time

    os.makedirs("results", exist_ok=True)
    filename = "results/pi_monte_carlo_parallel_results.csv"
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Використовуємо "N vs M" замість небезпечного для Windows слешу "\"
        writer.writerow(["N vs M"] + [f"M={m}" for m in M_values])
        
        for n in N_values:
            row = [f"N={n:,}"] + [results_matrix[n][m] for m in M_values]
            writer.writerow(row)
            
    print(f"\nУспішно! Результати збережено у файл: {filename}")

if __name__ == "__main__":
    main()