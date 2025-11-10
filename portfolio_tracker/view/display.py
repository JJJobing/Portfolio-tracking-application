import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date
import matplotlib
matplotlib.use("TkAgg")


class Display:
    def show_portfolio(self, data):
        """Print a simple overview of all holdings."""
        if not data:
            print("No assets in portfolio.\n")
            return
        print("\nPortfolio overview:")
        for row in data:
            print(f"{row['ticker']:>5} | {row['sector']:<12} | {row['asset_class']:<10} | "
                  f"Qty: {row['quantity']:>4} | Buy €{row['purchase_price']}")
        print()

    def show_market_data(self, data):
        """Print current market prices and returns."""
        if not data:
            print("No assets to show.\n")
            return
        print("\nCurrent market data:")
        for r in data:
            print(f"{r['ticker']}: "
                  f"Bought €{r['purchase_price']} | "
                  f"Now €{r.get('current_price')} | "
                  f"Value €{r.get('current_value')} | "
                  f"PnL €{r.get('gain_loss')} ({r.get('return_pct')}%)")
        print()

    def show_message(self, message):
        print(message)

    def show_portfolio_stats(self, stats):
        if not stats:
            print("No portfolio data available.\n")
            return

        print("\n----- Portfolio Summary -----")
        print(f"Total portfolio value: €{stats['total_value']}\n")

        print("Asset breakdown:")
        for r in stats["assets"]:
            print(f"{r['ticker']:<5} | Value: €{
                  r['current_value']:<10} | Weight: {r['weight']}%")

        print("\nBy sector:")
        for sec, w in stats["sector_weights"].items():
            print(f"{sec:<15}: {w}%")

        print("\nBy asset class:")
        for cls, w in stats["class_weights"].items():
            print(f"{cls:<15}: {w}%")

        print()

    def show_price_chart(self, tickers, start_date):
        """Plot historical prices from user-selected start date until today."""
        if not tickers:
            print("No tickers provided.\n")
            return

        plt.figure(figsize=(10, 5))
        end_date = date.today().strftime("%Y-%m-%d")

        for t in tickers:
            try:
                data = yf.Ticker(t).history(start=start_date, end=end_date)
                plt.plot(data.index, data["Close"], label=t)
            except Exception:
                print(f"Could not fetch data for {t}")

        plt.title(f"Historical Prices ({start_date} → {end_date})")
        plt.xlabel("Date")
        plt.ylabel("Price (€)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show(block=False)
        
    def show_volatility_chart(self, vol_dict, window):
        if not vol_dict:
            print("No volatility data available.\n")
            return
    
        import matplotlib
        matplotlib.use("TkAgg")
        import matplotlib.pyplot as plt
    
        plt.figure(figsize=(12, 6))
    
        # Keep last 3 years (252*3 trading days ≈ 756)
        DAYS_3Y = 756
    
        for ticker, series in vol_dict.items():
            trimmed = series.tail(DAYS_3Y)
            plt.plot(trimmed.index, trimmed.values, label=ticker)
    
        plt.title(f"{window}-Day Rolling Annualized Volatility (last 3 years)")
        plt.xlabel("Date")
        plt.ylabel("Volatility")
        plt.grid(True)
        plt.legend()
        plt.show(block=False)
        
    def show_correlation_heatmap(self, corr_matrix):
        if corr_matrix is None:
            print("Not enough data to compute correlations.\n")
            return
    
        import matplotlib
        matplotlib.use("TkAgg")
        import matplotlib.pyplot as plt
        import seaborn as sns
    
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            linewidths=0.5,
            square=True
        )
    
        plt.title("Asset Correlation Heatmap (3-Year Daily Returns)")
        plt.tight_layout()
        plt.show(block=False)

