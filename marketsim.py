 			     			  	 
import datetime as dt  		  	   		 	 	 			  		 			     			  	 
import os  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import numpy as np  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import pandas as pd  		  	   		 	 	 			  		 			     			  	 
from util import get_data, plot_data

import matplotlib.pyplot as plt

import scipy.optimize as spo


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return ""  # replace tb34 with your Georgia Tech username.


def gtid():
    """
    :return: The GT ID of the student
    :rtype: int
    """
    return  # replace with your GT ID number

def compute_portvals(
    orders_file="./orders/orders.csv",
    start_val=1000000,
    commission=9.95,
    impact=0.005,
):
    """  		  	   		 	 	 			  		 			     			  	 
    Computes the portfolio values.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    :param orders_file: Path of the order file or the file object  		  	   		 	 	 			  		 			     			  	 
    :type orders_file: str or file object  		  	   		 	 	 			  		 			     			  	 
    :param start_val: The starting value of the portfolio  		  	   		 	 	 			  		 			     			  	 
    :type start_val: int  		  	   		 	 	 			  		 			     			  	 
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		 	 	 			  		 			     			  	 
    :type commission: float  		  	   		 	 	 			  		 			     			  	 
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		 	 	 			  		 			     			  	 
    :type impact: float  		  	   		 	 	 			  		 			     			  	 
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		 	 	 			  		 			     			  	 
    :rtype: pandas.DataFrame  		  	   		 	 	 			  		 			     			  	 
    """
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    # start_date = dt.datetime(2008, 1, 1)
    # end_date = dt.datetime(2008, 6, 1)
    # portvals = get_data(["IBM"], pd.date_range(start_date, end_date))
    # portvals = portvals[["IBM"]]  # remove SPY
    # rv = pd.DataFrame(index=portvals.index, data=portvals.values)
    # return rv
    # return portvals

    # Load the Price data (adjusted prices) that was created previously
    # price_data = pd.read_csv('price.csv')  # This assumes you saved it as 'price.csv'

    # Load the orders file (orders-02.csv) that contains the buy/sell transactions
    #orders_data = pd.read_csv('/content/stock_data/orders-02.csv')
    orders= pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])

    syms = orders['Symbol'].unique()
    #print(syms)
    #orders.index = pd.to_datetime(orders['Date'])
    # get the start and end data
    # start_date = orders['Date'].min()
    # end_date = orders['Date'].max()
    start_date = orders.index.min()
    end_date = orders.index.max()
    dates=pd.date_range(start_date, end_date)
    # print('this is dates')
    # print(dates)
    dates_data = pd.DataFrame(dates, columns=['Date'])
    # print(dates_data)

    prices_all = get_data(syms, dates)
    prices = prices_all[syms]  # only portfolio symbols
    # prices['Cash']=1.0 #initiate cash value as 1.0
    # #prices['Date'] = prices.index

    # Reset the index to move the Date (index) into a column
    prices_data = prices.reset_index()
    # print("prices_data")
    # print(prices_data)

    #ffilled price data
    # prices_data.reset_index()
    # prices_data.rename(columns={'index':'Date'}, inplace=True)
    #
    # prices_data = pd.merge(dates_data, prices_data, on='Date', how='left')
    #
    # # Forward fill the portvalue column to fill missing values
    # prices_data['AAPL'] = prices_data['AAPL'].ffill()
    # prices_data['GOOG'] = prices_data['GOOG'].ffill()
    # prices_data['IBM'] = prices_data['IBM'].ffill()
    # prices_data['XOM'] = prices_data['XOM'].ffill()
    #
    # print("new_prices_data ffilled")
    # print(prices_data)

    # Rename the 'index' column to 'Date'
    prices_data = prices_data.rename(columns={'index': 'Date'})


    prices_melted = prices_data.melt(id_vars=['Date'], var_name='Symbol', value_name='Price')

    # Merge orders and prices tables
    daily_trades = pd.merge(orders, prices_melted, on=['Date', 'Symbol'])

    # # Calculate trade value
    # daily_trades['Trade Value'] = daily_trades['Shares'] * daily_trades['Price']


    # Calculate trade value with impact
    daily_trades['Trade Value'] = daily_trades.apply(
        lambda row: row['Shares'] * row['Price'] * (1 + impact) if row['Order'] == 'BUY' else row['Shares'] * row['Price'] * (1 - impact),
        axis=1
    )

    # Calculate cash flow for each trade including commission
    daily_trades['Cash Flow'] = daily_trades.apply(
        lambda row: -row['Trade Value'] - commission if row['Order'] == 'BUY' else row['Trade Value'] - commission,
        axis=1
    )



    # Sort by Date for better readability
    daily_trades = daily_trades.sort_values(by='Date').reset_index(drop=True)

    # Show the result
    #print(prices_reset)
    #print("prices")
    # print("daily_trades")
    # print(daily_trades.head(20))
    df = daily_trades.copy()
    # Calculate cash flow for each trade
    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    commission=9.95
    impact=0.005

    # Calculate cash flow for each trade
    df['Cash Flow'] = df.apply(lambda row: -row['Trade Value'] if row['Order'] == 'BUY' else row['Trade Value'], axis=1)

    #df['Cash Flow'] = df.apply(lambda row: -row['Trade Value'] * (1+ impact) - commission if row['Order'] == 'BUY' else row['Trade Value'] * (1-impact) - commission, axis=1)



    # Group by Date and sum the cash flow
    daily_cash_flow = df.groupby('Date')['Cash Flow'].sum().reset_index()

    # Set initial balance

    # Calculate cumulative cash flow including the initial balance
    daily_cash_flow['Cumulative Cash Flow'] = start_val + daily_cash_flow['Cash Flow'].cumsum()

    # Display the result
    # print("daily_cash_flow")
    # print(daily_cash_flow)

    #daily_cash_flow= pd.merge(dates_data, daily_cash_flow, on='Date', how='left')
    daily_cash_flow= pd.merge(prices_data, daily_cash_flow, on='Date', how='left')


    # Calculate the value of each stock on each day
    daily_cash_flow['Cash Flow'] = daily_cash_flow['Cash Flow'].ffill()
    daily_cash_flow['Cumulative Cash Flow'] = daily_cash_flow['Cumulative Cash Flow'].ffill()
    # print("new ffiled daily_cash_flow")
    # print(daily_cash_flow)

    df_orders = daily_trades.copy()

    # Convert 'Date' column to datetime
    df_orders['Date'] = pd.to_datetime(df_orders['Date'])

    # Calculate daily changes in shares for each symbol
    df_orders['Shares Change'] = df_orders.apply(lambda row: row['Shares'] if row['Order'] == 'BUY' else -row['Shares'], axis=1)

    # Group by Date and Symbol to calculate daily changes in shares
    daily_shares_change = df_orders.groupby(['Date', 'Symbol'])['Shares Change'].sum().reset_index()

    # Pivot the table to create a new order book
    order_book = daily_shares_change.pivot(index='Date', columns='Symbol', values='Shares Change').fillna(0)

    # Reset index to make Date a column
    order_book = order_book.reset_index()

    order_book[['AAPL', 'GOOG', 'IBM', 'XOM']] = order_book[['AAPL', 'GOOG', 'IBM', 'XOM']].cumsum()

    #
    # print("order_book")
    # print(order_book)

    new_prices_data = prices_data
    new_prices_data = prices_data.reset_index()
    new_prices_data_dates = new_prices_data[['Date']]


    # print('new_prices_data_dates')
    # print(new_prices_data_dates)

    order_book = pd.merge(new_prices_data_dates, order_book, on='Date', how='left')

    #order_book = pd.merge(dates_data, order_book, on='Date', how='left')

    # Forward fill the portvalue column to fill missing values
    order_book['AAPL'] = order_book['AAPL'].ffill()
    order_book['GOOG'] = order_book['GOOG'].ffill()
    order_book['IBM'] = order_book['IBM'].ffill()
    order_book['XOM'] = order_book['XOM'].ffill()
    # print("new_order_book")
    # print(order_book)

    # Assuming 'Symbol' and 'prices_data' are your DataFrames
    # Merge the DataFrames on the 'Date' column
    merged_data = pd.merge(order_book, prices_data, on='Date', how='left')

    # Calculate the value of each stock on each day
    merged_data['AAPL_value'] = merged_data['AAPL_x'] * merged_data['AAPL_y']
    merged_data['GOOG_value'] = merged_data['GOOG_x'] * merged_data['GOOG_y']
    merged_data['IBM_value'] = merged_data['IBM_x'] * merged_data['IBM_y']
    merged_data['XOM_value'] = merged_data['XOM_x'] * merged_data['XOM_y']

    # Sum the values of all stocks for each day to get the total portfolio value
    merged_data['Total_Value'] = merged_data[['AAPL_value', 'GOOG_value', 'IBM_value', 'XOM_value']].sum(axis=1)
    #merged_data=merged_data.fillna(method='ffill')

    # Display the result
    # print("new stock_value")
    # print(merged_data[['Date', 'AAPL_value', 'GOOG_value', 'IBM_value', 'XOM_value', 'Total_Value']])

    daily_cash_flow['portvalue'] = daily_cash_flow['Cumulative Cash Flow'] + merged_data['Total_Value']
    daily_cash_flow.set_index('Date')
    portfolio_vals = pd.DataFrame(daily_cash_flow)
    portfolio_vals= daily_cash_flow[['Date','portvalue']]
    portfolio_vals.set_index('Date', inplace = True)
    # print(portfolio_vals)

    #
    portvals = portfolio_vals
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    # print(portvals)
    return portvals


def test_code():
    """  		  	   		 	 	 			  		 			     			  	 
    Helper function to test code  		  	   		 	 	 			  		 			     			  	 
    """
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-02.csv"
    sv = 1000000
    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)
    # if isinstance(portvals, pd.DataFrame):
    #     portvals = portvals[portvals.columns[0]]  # just get the first column
    try:
        orders = pd.read_csv(of, index_col='Date', parse_dates=True, na_values=['nan'])
        # Check the first few rows to ensure data loaded correctly
        #print(orders.head())
    except Exception as e:
        print(f"An error occurred: {e}")
    start_date = orders.index.min()
    end_date = orders.index.max()
    dates=pd.date_range(start_date, end_date)
    syms = orders['Symbol'].unique()
    #print(syms)
    #dates_data = pd.DataFrame(dates, columns=['Date'])
    # print(dates_data)
    #
    prices_all = get_data(syms, dates)
    prices = prices_all[syms]  # only portfolio symbols
    # Reset the index to move the Date (index) into a column
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]
    # print(prices_SPY)
    prices_data = prices.reset_index()
    # print("prices_data")
    # print(prices_data)
    newdates = pd.to_datetime(prices_data['index'].values)

    # print(newdates)

    # # syms.append('$SPX')

    prices_SPX = get_data(['$SPX'], newdates,addSPY=False)  # only SPY, for comparison later
    prices_SPX = prices_SPX[prices_SPX.columns[0]]
    # prices_getSPX = prices_getSPX.reset_index()
    # prices_SPY
    # prices_getSPX.dropna()
    #prices_getSPX=prices_getSPX['$SPX']

    # prices_all_spx = get_data(syms, dates)
    # prices = prices_all[syms]  # only portfolio symbols

    # print("price_spx")
    # print(prices_SPX)

    # # Process orders
    # portvals = compute_portvals(orders_file=of, start_val=sv)
    # # if isinstance(portvals, pd.DataFrame):
    # #     portvals = portvals[portvals.columns[0]]  # just get the first column

    daily_rets = portvals.pct_change().dropna()
    cum_ret = portvals[-1] / portvals[0] - 1
    avg_daily_ret = np.mean(daily_rets)
    std_daily_ret = np.std(daily_rets)
    sharpe_ratio = np.sqrt(252) * (avg_daily_ret / std_daily_ret)


    # SPX returns
    spx_daily_rets = prices_SPX.pct_change().dropna()
    cum_ret_SPY = prices_SPX[-1] / prices_SPX[0] - 1
    avg_daily_ret_SPY = np.mean(spx_daily_rets)
    std_daily_ret_SPY = np.std(spx_daily_rets)
    sharpe_ratio_SPY = np.sqrt(252) * (avg_daily_ret_SPY / std_daily_ret_SPY)

    # Compare portfolio against $SPX
    print(f"Date Range: {start_date} to {end_date}")
    print()
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")
    print()
    print(f"Cumulative Return of Fund: {cum_ret}")
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")
    print()
    print(f"Standard Deviation of Fund: {std_daily_ret}")
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")
    print()
    print(f"Average Daily Return of Fund: {avg_daily_ret}")
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")
    print()
    print(f"Final Portfolio Value: {portvals[-1]}")


  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
if __name__ == "__main__":  		  	   		 	 	 			  		 			     			  	 
    test_code()  		  	   		 	 	 			  		 			     			  	 
