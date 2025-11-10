import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use("TkAgg")

class MonteCarloView:

    def show_basic_results(self, sim):
        print("\n----- Monte Carlo Simulation Results -----")
        print(f"Median final value:     €{sim['median']:.2f}")
        print(f"Mean final value:       €{sim['mean']:.2f}")
        print(f"VaR (5%):               €{sim['var5']:.2f}")
        print(f"Expected Shortfall (5%): €{sim['es5']:.2f}")
        print(f"95th percentile:        €{sim['p95']:.2f}")

    def show_histogram(self, sim):
        if sim is None or "final_values" not in sim:
            print("Run a simulation first.")
            return
    
        values = sim["final_values"]
    
        plt.figure(figsize=(10, 5))
        plt.hist(values, bins=50, edgecolor="black", color="lightblue")
    
        plt.axvline(sim["var5"], color="red", linestyle="--", linewidth=1.5, label="VaR 5%")
        plt.axvline(sim["es5"], color="purple", linestyle="--", linewidth=1.5, label="ES 5%")
    
        plt.title("Distribution of Final Portfolio Value with MC simulation")
        plt.xlabel("Portfolio Value (€)")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True)
    
        plt.show(block=False)   



    def show_fan_chart(self, bands):
        if bands is None:
            print("Run a simulation first.")
            return
    
        p5 = np.array(bands["p5"])
        p50 = np.array(bands["p50"])
        p95 = np.array(bands["p95"])
    
        # Additional percentiles
        p25 = np.array(bands["p25"])
        p75 = np.array(bands["p75"])
        p975 = np.array(bands["p975"])
        p25 = np.array(bands["p25"])
        p75 = np.array(bands["p75"])
    
        t = np.linspace(0, 15, len(p50))
    
        plt.figure(figsize=(12, 6))
    
        # 95% band (lightest)
        plt.fill_between(t, bands["p025"], bands["p975"], 
                         color="blue", alpha=0.25, label="95% band")
    
        # 90% band
        plt.fill_between(t, p5, p95, 
                         color="blue", alpha=0.35, label="90% band")
    
        # 50% band (darkest)
        plt.fill_between(t, p25, p75, 
                         color="blue", alpha=0.55, label="50% band")
    
        # Median
        plt.plot(t, p50, color="black", linewidth=2.0, label="Median")
    
        plt.title("15-Year Forecast Fan Chart with MC simulation")
        plt.xlabel("Years")
        plt.ylabel("Portfolio Value (€)")
        plt.grid(True)
        plt.legend()
        plt.show(block=False)

