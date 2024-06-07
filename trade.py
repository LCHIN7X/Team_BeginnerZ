import requests
import time

ticker = "MSFT"
api_key ="a74c1d6a9bfc48a096826ab16608dd72"

def get_stock_price(ticker_symbol,api):
    url = f"https://api.twelvedata.com/price?symbol={ticker_symbol}&apikey={api}"
    responese = requests.get(url).json()
    price = responese['price'][:-3]

    print(price)
    return price

def get_stock_quote(ticker_symbol,api):
    url = f"https://api.twelvedata.com/quote?symbol={ticker_symbol}&apikey={api}"
    responese = requests.get(url).json()
    return responese

name = get_stock_quote(ticker,api_key)['name']
stock_price = get_stock_price(ticker,api_key)

print(name,stock_price)