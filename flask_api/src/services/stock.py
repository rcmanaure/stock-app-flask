# from os import abort
from flask import Blueprint,abort
from flasgger import swag_from
from .app import db, Transaction
from webargs.flaskparser import use_args
from marshmallow import fields
import requests


# Init the Blueprints of be used in the authorization routes.
stock = Blueprint('stock', __name__)


# @stock.route('/ticker')
def get_data(ticker:str):   
    res = requests.get("https://api.nasdaq.com/api/quote/{ticker}/info?assetclass=stocks".format(ticker=ticker),headers={
"User-Agent" : "Mozilla/5.0"}).json()    
    
    return res

@stock.route('/buy-stock/', methods=['POST'])
@swag_from('./docs/stock/post.yaml')
@use_args({'ticker':fields.String(),'qty':fields.Integer() })
# Buy a number of shares of a certain stock via its symbol
def buy_shares(args:dict):   
    get_ticker = get_data(args['ticker']) 
    if args['ticker'] == get_ticker['data']['symbol']:
        print(get_ticker)
        print(get_ticker['data']['primaryData']['lastSalePrice'])
        ticker= get_ticker['data']['symbol']
        qty=args['qty']  
        name = get_ticker['data']['companyName']
        price = round(float(2),2)
        txn_amount = price * qty     
        
        txn = Transaction.query.filter_by(ticker=ticker).first()
        # print(share)
        if txn is not None:
            txn.qty += qty
            db.session.commit()   
        else:    
            new_tras= Transaction(ticker=ticker,name=name, qty=qty, last_price=txn_amount)
            db.session.add(new_tras)
            db.session.commit()
        return 'Succesful'
    else:
        abort(400, 'Symbol not exists on the NASDAQ API')
    

@stock.route('/sell_stock', methods=['POST'])
@swag_from('./docs/stock/sell_stocks.yaml')
@use_args({'ticker':fields.String(),'qty':fields.Integer() })
# Sell a number of shares of a certain stock via its symbol
def sell_share(args:dict):
    get_ticker = get_data(args['ticker']) 
    if args['ticker'] == get_ticker['data']['symbol']:
        ticker= get_ticker['data']['symbol']
        qty=args['qty']          
        price = round(float(2),2)       
        
        txn = Transaction.query.filter_by(ticker=ticker).first()
        
        qtyAvailable = db.session.query(db.func.sum(Transaction.qty)).filter(
                                        Transaction.ticker==ticker).first()[0]
        
        if qty > qtyAvailable:            
            return 'Not enough shares'        
        elif txn is not None:
            txn.qty -= qty
            db.session.commit() 
            return 'Succesful'
        else:
            return 'Error selling shares, check parameters'
    else:
        abort(400, 'Symbol not exists on the NASDAQ API')   

@stock.route('/stock-prices', methods=['GET'])
@swag_from('./docs/stock/get_price.yaml')
# @use_args({"price": fields.String}, location="view_args")
# Get the historic price of a stock you bought
def stock_price():
    
    return 'price'