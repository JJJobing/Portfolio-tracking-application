Vermogensbeheer Assignment A.S.R.

This portfolio tracker allows the user to edit his portfolio and get analytics about the portfolio and individual assets. The tracker can be opened using a CLI. By typing "python3 -m main" the application is opened and the user can use it.
Below the menu options are treated seperately on their function and how to use them. 

1. Add or remove an asset
This option is used to add or remove individual assets in the portfolio. It has a sub-menu:

  1. Add asset
  This function allows the user to type in the ticker of the asset he would like to add to the portfolio. He will receive information about the sector, asset class and current market price, which is imported from Yahoo Finance. Then the user chooses the quantity he wants for the asset. 
  
  2. Delete asset
  This is used when the user wants to delete an asset from the portfolio. This is done by typing in the ticker of the asset. 
  
  3. Back to main menu
  After performing mutations on the portfolio the user can return to the main menu. 

2. View portfolio
This option allows the user to get an overview of the portfolio. This will show all the tickers with the quantity, sector, asset type and buy price. 

3. Show price history and graph
With this option the user can create a graph with historical data of the portfolio. The user can choose which asset he wants to see or that he wants all of the assets in one graph. Also the starting date is asked as input from the user. 

4. See portfolio calculations
This option is used to get insight in the portfolio weights. The full portfolio value is given with the weights of the assets. Also the weight per sector and asset class are given to the user. 

5. Monte Carlo simulations
With this option the user gets a menu with options for Monte Carlo simulations. These are simulations for the upcoming 15 years with 100,000 simulated paths. This takes some time in computation. The sub-menu here is given by:

  1. Run Monte Carlo (Normal distribution)
  2. Run Monte Carlo (Student-t distribution)
  
  These options will run a MC simulation, but the user can choose between two different distributions, normal and Student-t. Then the mean and median value, the Value-at-Risk and Expected Shortfall at 5% and the 95th percentile be presented to the user. The assignment asked for 15 years and 100,000 simulations, but becomes computationally expensive quickly. 
  
  3. Show fan chart
  With this function the user can create a fan chart after he ran a MC simulation. This fan chart shows the how the 50%, 90% and 95% percentiles develop in the simulation. 
  4. Show histogram
  With this option the user can create a histogram of the simulation he did. The VaR and ES at 5% level are also shown in this figure. 
  5. Back to main menu
  With this option the user goes back to the main menu.

6. Volatility Analysis
With this option the user can generate a figure showing the volatility. The user can choose a 5 day, 30 day or 90 day rolling window for the volatility and this is plotted for the last three years. With this function the user gets insights in possible volatility clustering in his portfolio. 

7. Asset Correlation Analysis
With this option the user can generate a correlation matrix showing how much each of the assets is correlated with each other. This way the user can see how much of his portfolio is correlated with each other. Diversification is in general advised to spread risk. 

8. Clear portfolio
This function cleans the full portfolio and deletes all the information about the assets from the data csv.

9. Exit
With this option the user exits the application. 
