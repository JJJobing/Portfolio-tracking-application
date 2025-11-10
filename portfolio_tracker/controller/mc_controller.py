from view.mc_view import MonteCarloView


class MonteCarloController:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.view = MonteCarloView()

    def run(self):
        while True:
            print("\n--- Monte Carlo Simulation Menu ---")
            print("1. Run Monte Carlo (Normal distribution)")
            print("2. Run Monte Carlo (Student-t distribution)")
            print("3. Show fan chart")
            print("4. Show histogram")
            print("5. Back to main menu")

            choice = input("Choose an option: ")

            if choice == "1":
                self.last_dist = "normal"
                self.sim = self.portfolio.simulate_portfolio(dist="normal")
                self.view.show_basic_results(self.sim)

            elif choice == "2":
                self.last_dist = "t"
                self.sim = self.portfolio.simulate_portfolio(dist="t")
                self.view.show_basic_results(self.sim)


            elif choice == "3":
                bands = self.portfolio.simulate_fan_chart(dist=getattr(self, "last_dist", "normal"))
                if not bands:
                    print("No data. Add assets first.")
                else:
                    self.view.show_fan_chart(bands)
            

            elif choice == "4":
                if hasattr(self, "sim"):
                    self.view.show_histogram(self.sim)
                else:
                    print("Run a simulation first.")

            elif choice == "5":
                return

            else:
                print("Invalid choice.")
