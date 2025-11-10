from model.portfolio import Portfolio
from controller.mc_controller import MonteCarloController
from view.display import Display
import yfinance as yf
from datetime import datetime


class Controller:
    def __init__(self):
        self.portfolio = Portfolio()
        self.view = Display()

    def run(self):
        while True:
            print("\n----- Portfolio Tracker -----")
            print("1. Add or remove an asset")
            print("2. View portfolio")
            print("3. Show price history and graph")
            print("4. See portfolio calculations")
            print("5. Monte Carlo simulations")
            print("6. Volatility Analysis")
            print("7. Asset Correlation Analysis")
            print("8. Clear portfolio")
            print("9. Exit")
    
            choice = input("Choose an option: ")
    
            if choice == "1":
                self.manage_asset()
            elif choice == "2":
                data = self.portfolio.read_portfolio()
                self.view.show_portfolio(data)
            elif choice == "3":
                self.show_price_graph()
            elif choice == "4":
                stats = self.portfolio.summary_stats()
                self.view.show_portfolio_stats(stats)
            elif choice == "5":
                mc = MonteCarloController(self.portfolio)
                mc.run()
            elif choice == "6":
                self.show_volatility_analysis()
            elif choice == "7":
                self.show_correlation_analysis()
            elif choice == "8":
                self.portfolio.clear_portfolio()
                self.portfolio = Portfolio()
            elif choice == "9":
                print("Goodbye!")
                break



    def manage_asset(self):
        print("\n--- Asset Manager ---")
        print("1. Add asset")
        print("2. Delete asset")
        print("3. Back to main menu")
    
        choice = input("Choose an option: ")
    
        # Add an asset
        if choice == "1":
            print("\n--- Add New Asset ---")
    
            ticker = input("Ticker: ").upper()
    
            try:
                info = yf.Ticker(ticker).info
                sector = info.get("sector", "Unknown")
                asset_class = "Equity"  # Assume equities for now
                current_price = round(info.get("currentPrice", 0), 2)
    
                print(f"\n{ticker} information:")
                print(f"Sector: {sector}")
                print(f"Asset class: {asset_class}")
                print(f"Current market price: €{current_price}")
            except Exception:
                print("\nCould not fetch data for this ticker.")
                sector = "Unknown"
                asset_class = "Unknown"
                current_price = 0
    
            try:
                quantity = float(input("\nQuantity to add: "))
            except ValueError:
                self.view.show_message("Invalid quantity.\n")
                return
    
            # Use current market price as purchase price
            price = current_price if current_price else float(input("Purchase price: "))
    
            self.portfolio.add_asset(ticker, sector, asset_class, quantity, price)
            self.view.show_message(f"{ticker} added to portfolio.\n")
    
        # Delete an asset
        elif choice == "2":
            print("\n--- Delete Asset ---")
            ticker = input("Enter ticker to delete: ").upper()
    
            deleted = self.portfolio.delete_asset(ticker)
            if deleted:
                print(f"{ticker} was deleted from the portfolio.\n")
            else:
                print(f"{ticker} not found in portfolio.\n")
    
        # Go back to menu
        elif choice == "3":
            return
        else:
            print("Invalid option.\n")

        
        
    def show_price_graph(self):
        data = self.portfolio.read_portfolio()
        tickers = [row["ticker"] for row in data]

        if not tickers:
            self.view.show_message("No tickers in portfolio.\n")
            return

        print("\nTickers in your portfolio:")
        for i, t in enumerate(tickers, 1):
            print(f"{i}. {t}")

        choice = input("Enter ticker numbers separated by commas (or 'all'): ").strip()

        if choice.lower() == "all":
            selected = tickers
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(",")]
                selected = [tickers[i] for i in indices if 0 <= i < len(tickers)]
            except ValueError:
                self.view.show_message("Invalid selection.\n")
                return

        # Ask for start date
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()

        # Basic validation for format
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            self.view.show_message("Invalid date format. Please use YYYY-MM-DD.\n")
            return

        self.view.show_price_chart(selected, start_date)
        
    def show_volatility_analysis(self):
        print("\n--- Volatility Analysis ---")
        print("Choose rolling window:")
        print("1. 5 days")
        print("2. 30 days")
        print("3. 90 days")
    
        opt = input("Enter option: ")
    
        if opt == "1":
            window = 5
        elif opt == "2":
            window = 30
        elif opt == "3":
            window = 90
        else:
            print("Invalid option.\n")
            return
    
        vol = self.portfolio.rolling_volatility(window)
        self.view.show_volatility_chart(vol, window)
        
    def show_correlation_analysis(self):
        corr = self.portfolio.asset_correlation()
        self.view.show_correlation_heatmap(corr)


