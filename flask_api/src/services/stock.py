from flask import Blueprint, render_template, redirect, url_for, request, flash
from flasgger import swag_from
from .app import db, Transaction
from webargs.flaskparser import use_args
from marshmallow import (fields)


# Init the Blueprints of be used in the authorization routes.
stock = Blueprint('stock', __name__)

@stock.route('/buy-stock/', methods=['POST'])
@swag_from('./docs/stock/post.yaml')
@use_args({'ticker':fields.String(),'qty':fields.Integer() })
# Buy or sell a number of shares of a certain stock via its symbol
def buy_shares(args:dict):    
    ticker= args['ticker']
    qty=args['qty']  
    name = 'pepe'
    price = round(float(2),2)
    txn_Amount = price * qty     
    
    share = Transaction.query.filter_by(ticker=ticker).first()
    print(share)
    if share is not None:
        share.qty += qty
        db.session.commit()   
    else:    
        new_tras= Transaction(ticker=ticker,name=name, qty=qty, price=txn_Amount)
        db.session.add(new_tras)
        db.session.commit()
    return 'Succesful'
    

@stock.route('/sell_stock', methods=['POST'])
@swag_from('./docs/stock/sell_stocks.yaml')
@use_args({'ticker':fields.String(),'qty':fields.Integer() })
# Get a list of the stocks you are holding
def sell_share(args:dict):
    ticker= args['ticker']
    qty=args['qty']  
    name = 'pepe'
    price = round(float(2),2)
    txnAmount = price * qty  
    qtyAvailable = db.session.query(db.func.sum(Transaction.qty)).filter(
                                    Transaction.ticker==ticker).first()[0]
    
    if qty > qtyAvailable:
        return False
    new_tras = Transaction(ticker=ticker, name=name, qty=-qty, price=txnAmount)
    db.session.add(new_tras)
    db.session.commit()
    return 'True'

@stock.route('/stock-prices', methods=['GET'])
@swag_from('./docs/stock/get_price.yaml')
# @use_args({"price": fields.String}, location="view_args")
# Get the historic price of a stock you bought
def stock_price():
    
    return 'price'