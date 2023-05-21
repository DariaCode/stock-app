from flask import Blueprint, jsonify
import yfinance as finance
from api.stock_utils import calculate_stock_data, calculate_cumulative_return, calculate_annualized_return, calculate_annualized_volatility, calculate_performance


api_bp = Blueprint('api', __name__)

@api_bp.route('/stocks', methods=['GET'])
def stocks():
    stocks = ['AAPL', 'MSFT', 'TSLA']
    stock_data = {}

    for stock in stocks:
        data = finance.Ticker(stock).history(period='1y')
        initial_price = data['Close'][0]
        stock_data[stock] = calculate_stock_data(data, initial_price)

    return jsonify(stock_data)

@api_bp.route('/stock/<stockName>', methods=['GET'])
def stock(stockName):
    data = finance.Ticker(stockName).history(period='1y')
    initial_price = data['Close'][0]
    stock_data = calculate_stock_data(data, initial_price)

    return jsonify(stock_data)

@api_bp.route('/performances', methods=['GET'])
def performances():
    stocks = ['AAPL', 'MSFT', 'TSLA']
    stocks_performance ={}

    for stock in stocks:
        stock_data = finance.download(stock, period='5y')
        stock_data_year = finance.download(stock, period='1y')
        stocks_performance[stock] = calculate_performance(stock_data, stock_data_year)

    return jsonify(stocks_performance)

@api_bp.route('/performance/<stockName>', methods=['GET'])
def performance(stockName):
    stock_data = finance.download(stockName, period='5y')
    stock_data_year = finance.download(stockName, period='1y')
    stock_performance = calculate_performance(stock_data, stock_data_year)

    return jsonify(stock_performance)
