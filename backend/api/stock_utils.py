import numpy as np
import pandas as pd
from decimal import Decimal

def calculate_stock_data(data, initial_price):
    stock_data = [
        {
            'date': str(date),
            'value': round((close / initial_price) * 100, 2),
            'price': close
        }
        for date, close in zip(data.index, data['Close'])
    ]

    return stock_data

def calculate_performance(data, data_year):
    cumulative_return = calculate_cumulative_return(data)
    annualized_return = calculate_annualized_return(cumulative_return, 5)
    annualized_volatility = calculate_annualized_volatility(data_year)

    stock_performance = {
        'cumulative_return': cumulative_return * 100,
        'annualized_return': annualized_return * 100,
        'annualized_volatility': annualized_volatility * 100
    }

    return stock_performance
    

def calculate_cumulative_return(data):
    start_price = Decimal(data.iloc[0]['Close'])
    end_price = Decimal(data.iloc[-1]['Close'])
    total_return = end_price - start_price
    cumulative_return = (total_return / start_price) 

    return round(cumulative_return, 2)

def calculate_annualized_return(cumulative_return, years):
    annualized_return = ((1 + cumulative_return) ** Decimal(1) / Decimal(years)) - 1

    return round(annualized_return, 2)

def calculate_annualized_volatility(data):
    data['Daily Return'] = data['Close'].pct_change()
    volatility = Decimal(str(data['Daily Return'].std()))
    trading_days_per_year = 252
    annualized_volatility = volatility * (Decimal(trading_days_per_year) ** Decimal('0.5'))

    return round(annualized_volatility, 2)