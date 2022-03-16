from flask import Blueprint,request,jsonify
from flasgger import swag_from
from .app import db, Transaction
from webargs.flaskparser import use_args
from marshmallow import fields
import requests
import json

# Init the Blueprints of be used in the authorization routes.
stock = Blueprint('stock', __name__)



def get_data(ticker:str):   
    res = requests.get("https://api.nasdaq.com/api/quote/{ticker}/info?assetclass=stocks".format(ticker=ticker),headers={
"User-Agent" : "Mozilla/5.0"}).json()    
    
    return res

@stock.route('/share/', methods=['POST', 'PUT'])
@use_args({'ticker':fields.String(),'qty':fields.Integer() })
# Buy/Sell a number of shares of a certain stock via its symbol
def buy_shares(args:dict): 
    get_ticker = get_data(args['ticker'])
    if get_ticker['data'] is not None:    
        if request.method == 'POST': 
            # Buy share             
            if args['ticker'] == get_ticker['data']['symbol']:
                print(get_ticker)
                print(get_ticker['data']['primaryData']['lastSalePrice'])
                ticker= get_ticker['data']['symbol']
                qty=args['qty']  
                name = get_ticker['data']['companyName']
                price = get_ticker['data']['primaryData']['lastSalePrice']
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
                return 'Buy Succesful'
            else:
                return ('Buy Failed') 
        elif request.method == 'PUT':
            # Sell share
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
                    return 'Sell Succesful'
                else:
                    return 'Error selling shares, check parameters'
        else:
            return ('Sell Failed.') 
    else: 
        return get_ticker

@stock.route('/list-shares', methods=['GET'])
# @use_args({'ticker':fields.String(),'qty':fields.Integer() })
# Sell a number of shares of a certain stock via its symbol
def list_shares():
    publications = Transaction.query.all()
    prueba = publications
    print(prueba)
    return 'jsonify(publications)'
    # get_ticker = get_data(args['ticker']) 
    # if args['ticker'] == get_ticker['data']['symbol']:
    #     ticker= get_ticker['data']['symbol']
    #     qty=args['qty']          
    #     price = round(float(2),2)       
        
    #     txn = Transaction.query.filter_by(ticker=ticker).first()
        
    #     qtyAvailable = db.session.query(db.func.sum(Transaction.qty)).filter(
    #                                     Transaction.ticker==ticker).first()[0]
        
    #     if qty > qtyAvailable:            
    #         return 'Not enough shares'        
    #     elif txn is not None:
    #         txn.qty -= qty
    #         db.session.commit() 
    #         return 'Succesful'
    #     else:
    #         return 'Error selling shares, check parameters'
    # else:
    #     return ('Symbol not exists on the NASDAQ API')    

@stock.route('/stock-prices', methods=['GET','POST'])
@use_args({"price": fields.String()}, location="view_args")
# Get the historic price of a stock you bought
def stock_price(args):
    
    return 'price'