import csv
import numpy as np
from pathlib import Path
import yfinance as yf
from scipy.stats import t as student_t
import pandas as pd



class Portfolio:
    def __init__(self):
        # Point to the CSV file inside the data folder
        root = Path(__file__).resolve().parent.parent
        self.csv_path = root / "data" / "portfolio_data.csv"

        # Create the CSV file for saving the portfolio data
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.csv_path.exists():
            with self.csv_path.open("w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["ticker", "sector", "asset_class", "quantity", "purchase_price"])

    # Add an asset by filling in the ticker
    def add_asset(self, ticker, sector, asset_class, quantity, purchase_price):
        """Add a new position to the portfolio."""
        with self.csv_path.open("a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([ticker, sector, asset_class, quantity, purchase_price])
        print(f"Added {ticker}")
    
    # Delete an asset from the portfolio by giving the ticker
    def delete_asset(self, ticker):
        rows = self.read_portfolio()
        ticker = ticker.upper()
    
        new_rows = [r for r in rows if r["ticker"].upper() != ticker]
    
        if len(new_rows) == len(rows):
            return False
    
        with self.csv_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ticker", "sector", "asset_class", "quantity", "purchase_price"])
            for r in new_rows:
                writer.writerow([
                    r["ticker"],
                    r["sector"],
                    r["asset_class"],
                    r["quantity"],
                    r["purchase_price"]
                ])
        return True

    # Read out the portfolio and give information
    def read_portfolio(self):
        """Return all rows from the portfolio file."""
        with self.csv_path.open("r", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    # Clear the full portfolio
    def clear_portfolio(self):
        """Remove all assets and reset the CSV header."""
        with self.csv_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ticker", "sector", "asset_class", "quantity", "purchase_price"])

    # Get the current prices of the portfolio assets
    def current_prices(self):
        """Get the latest market price for each ticker."""
        rows = self.read_portfolio()
        for r in rows:
            ticker = r["ticker"]
            try:
                data = yf.Ticker(ticker).history(period="1d")
                r["current_price"] = round(data["Close"].iloc[-1], 2)
            except Exception:
                r["current_price"] = None
        return rows

    # Get the gain/loss at this moment for each asset
    def current_values(self):
        """Calculate the current value, gain/loss, and return for each asset."""
        rows = self.current_prices()
        for r in rows:
            qty = float(r["quantity"])
            buy_price = float(r["purchase_price"])
            cur_price = r.get("current_price")
            if cur_price:
                r["current_value"] = round(qty * cur_price, 2)
                r["gain_loss"] = round((cur_price - buy_price) * qty, 2)
                r["return_pct"] = round((cur_price / buy_price - 1) * 100, 2)
            else:
                r["current_value"] = None
                r["gain_loss"] = None
                r["return_pct"] = None
        return rows
    
    # Get summary statistics for the full portfolio, including the weights
    def summary_stats(self):
        """Return total portfolio value and weights per asset, sector, and class."""
        rows = self.current_values()
    
        # Filter out rows without current values
        rows = [r for r in rows if r.get("current_value")]
    
        if not rows:
            return None
    
        total_value = sum(r["current_value"] for r in rows)
    
        # Calculate individual weights
        for r in rows:
            r["weight"] = round((r["current_value"] / total_value) * 100, 2)
    
        # Group by sector
        sectors = {}
        for r in rows:
            sec = r["sector"]
            sectors[sec] = sectors.get(sec, 0) + r["current_value"]
    
        # Group by asset class
        classes = {}
        for r in rows:
            cls = r["asset_class"]
            classes[cls] = classes.get(cls, 0) + r["current_value"]
    
        # Compute weights for each group
        sector_weights = {k: round((v / total_value) * 100, 2) for k, v in sectors.items()}
        class_weights = {k: round((v / total_value) * 100, 2) for k, v in classes.items()}
    
        return {
            "total_value": round(total_value, 2),
            "assets": rows,
            "sector_weights": sector_weights,
            "class_weights": class_weights,
        }
    
    # Function for a rolling window volatility calculation
    def rolling_volatility(self, window=30):
        rows = self.current_values()
        rows = [r for r in rows if r.get("current_value")]
        if not rows:
            return None
    
        tickers = [r["ticker"] for r in rows]
        result = {}
    
        
        for ticker in tickers:
            data = yf.Ticker(ticker).history(period="5y")  
            if data.empty:
                continue
    
            returns = data["Close"].pct_change().dropna()
            rolling_vol = returns.rolling(window).std() * (252 ** 0.5)
            result[ticker] = rolling_vol
    
        return result
    
    
    def asset_correlation(self):
        """
        Returns a correlation matrix of daily returns for the current portfolio assets.
        Uses 3 years of daily data.
        """
        rows = self.current_values()
        tickers = [r["ticker"] for r in rows]
    
        if len(tickers) < 2:
            return None  
        
        prices = pd.DataFrame()
    
        # Fetch 3 years of daily close prices
        for t in tickers:
            data = yf.Ticker(t).history(period="3y")["Close"]
            if not data.empty:
                prices[t] = data
    
        if prices.empty or prices.shape[1] < 2:
            return None
    
        # Compute daily returns
        returns = prices.pct_change().dropna()
    
        # Correlation matrix
        corr_matrix = returns.corr()
    
        return corr_matrix


    
    def simulate_portfolio(self, years=15, paths=100_000, dist="normal", corr=True):
        """
        Monte Carlo simulation of FINAL portfolio value after 15 years.
        Returns VaR/ES, and the final-values distribution.
        Correlation via Cholesky of the correlation matrix.
        """
        rows = self.current_values()
        rows = [r for r in rows if r.get("current_value")]
        if not rows:
            return None

        tickers = [r["ticker"] for r in rows]
        p0 = np.array([r["current_price"] for r in rows], dtype=float)
        v0 = np.array([r["current_value"] for r in rows], dtype=float)
        port0 = float(v0.sum())
        weights = v0 / port0

        # Estimate daily log-return stats from history
        rets = []
        for t in tickers:
            h = yf.Ticker(t).history(period="5y")
            r = np.log(h["Close"] / h["Close"].shift(1)).dropna().values
            rets.append(r)

        # Align lengths 
        maxlen = max(len(r) for r in rets)
        aligned = [np.pad(r, (maxlen - len(r), 0), mode="edge") for r in rets]
        R = np.vstack(aligned).T  # shape (T, N)

        mu = R.mean(axis=0)         # daily mean
        sigma = R.std(axis=0)       # daily std

        # Correlation so we can scale by sigma once in the SDE
        if corr and len(tickers) > 1:
            C = np.corrcoef(R.T)
            try:
                L = np.linalg.cholesky(C)
            except np.linalg.LinAlgError:
                eps = 1e-10
                L = np.linalg.cholesky(C + eps * np.eye(C.shape[0]))
        else:
            L = np.eye(len(tickers))

        # Simulate geometric Brownian motion 
        days = int(years * 252)
        dt = 1.0 / 252.0

        if dist == "normal":
            Z = np.random.normal(0.0, 1.0, (paths, days, len(tickers)))
        else:
            # Student-t standardized to unit variance: t(df)/sqrt(df/(df-2))
            df = 5
            Z = student_t.rvs(df=df, size=(paths, days, len(tickers))) / np.sqrt(df / (df - 2))

        # Apply correlation to the *standard-normal* shocks
        Z = Z @ L.T  

        # Simulate final price for each asset, then combine by weights
        finals = np.zeros((paths, len(tickers)), dtype=float)
        for i, (p0_i, mu_i, sig_i) in enumerate(zip(p0, mu, sigma)):
            # Daily growth factors for this asset for all paths
            g = np.exp((mu_i - 0.5 * sig_i * sig_i) * dt + sig_i * np.sqrt(dt) * Z[:, :, i])
            finals[:, i] = p0_i * g.prod(axis=1)

        final_values = (finals * weights).sum(axis=1)  

        # Risk metrics on final values
        var5 = float(np.percentile(final_values, 5))
        es5 = float(final_values[final_values <= var5].mean())

        return {
            "final_values": final_values,
            "median": float(np.median(final_values)),
            "mean": float(final_values.mean()),
            "var5": var5,
            "es5": es5,
            "p025": float(np.percentile(final_values, 2.5)),
            "p25": float(np.percentile(final_values, 25)),
            "p50": float(np.percentile(final_values, 50)),
            "p75": float(np.percentile(final_values, 75)),
            "p95": float(np.percentile(final_values, 95)),
            "p975": float(np.percentile(final_values, 97.5))
        }
    
    def simulate_fan_chart(self, years=15, paths=2000, dist="normal", corr=True):
        """
        Returns percentile bands of the portfolio value over time.
        """
        rows = self.current_values()
        rows = [r for r in rows if r.get("current_value")]
        if not rows:
            return None
    
        tickers = [r["ticker"] for r in rows]
        p0 = np.array([r["current_price"] for r in rows], dtype=float)
        v0 = np.array([r["current_value"] for r in rows], dtype=float)
        port0 = float(v0.sum())
        weights = v0 / port0
    
        # Estimate statistics
        rets = []
        for t in tickers:
            h = yf.Ticker(t).history(period="5y")
            r = np.log(h["Close"] / h["Close"].shift(1)).dropna().values
            rets.append(r)
    
        maxlen = max(len(r) for r in rets)
        aligned = [np.pad(r, (maxlen - len(r), 0), mode="edge") for r in rets]
        R = np.vstack(aligned).T
    
        mu = R.mean(axis=0)
        sigma = R.std(axis=0)
    
        if corr and len(tickers) > 1:
            C = np.corrcoef(R.T)
            try:
                L = np.linalg.cholesky(C)
            except np.linalg.LinAlgError:
                L = np.linalg.cholesky(C + 1e-10 * np.eye(C.shape[0]))
        else:
            L = np.eye(len(tickers))
    
        days = int(years * 252)
        dt = 1.0 / 252.0
    
        if dist == "normal":
            Z = np.random.normal(0.0, 1.0, (paths, days, len(tickers)))
        else:
            df = 5
            Z = student_t.rvs(df=df, size=(paths, days, len(tickers))) / np.sqrt(df / (df - 2))
    
        Z = Z @ L.T  # correlate
    
        # Build portfolio paths directly to save memory
        port_paths = np.zeros((paths, days), dtype=np.float32)
    
        for i, (p0_i, mu_i, sig_i, w_i) in enumerate(zip(p0, mu, sigma, weights)):
            g = np.exp((mu_i - 0.5 * sig_i * sig_i) * dt + sig_i * np.sqrt(dt) * Z[:, :, i])  # (paths, days)
            price_paths_i = p0_i * np.cumprod(g, axis=1)
            port_paths += (w_i * price_paths_i).astype(np.float32)
    
        # Percentile bands across paths, for each day
        p025 = np.percentile(port_paths, 2.5, axis=0)
        p5   = np.percentile(port_paths, 5, axis=0)
        p25  = np.percentile(port_paths, 25, axis=0)
        p50  = np.percentile(port_paths, 50, axis=0)
        p75  = np.percentile(port_paths, 75, axis=0)
        p95  = np.percentile(port_paths, 95, axis=0)
        p975 = np.percentile(port_paths, 97.5, axis=0)
        
        return {
            "p025": p025,
            "p5": p5,
            "p25": p25,
            "p50": p50,
            "p75": p75,
            "p95": p95,
            "p975": p975
        }
