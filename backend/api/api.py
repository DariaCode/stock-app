from flask import Blueprint, jsonify
import yfinance as finance

api_bp = Blueprint('api', __name__)

@api_bp.route('/stocks', methods=['GET'])
def stocks():
    symbols = ['AAPL', 'MSFT', 'TSLA']
    stock_data = {}

    for symbol in symbols:
        stock = finance.Ticker(symbol)
        history = stock.history(period='1y')

        dates = history.index.strftime('%Y-%m-%d').tolist()
        prices = history['Close'].tolist()

        stock_data[symbol] = {'dates': dates, 'prices': prices}

    return jsonify(stock_data)
