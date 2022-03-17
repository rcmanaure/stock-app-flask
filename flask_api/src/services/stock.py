from flask import Blueprint,request,jsonify,make_response
from services.schema.list import StockResponseSchema
from .app import db, Transaction
from webargs.flaskparser import use_args
from marshmallow import fields
import requests
import json

# Init the Blueprints of be used in the stock routes.
stock = Blueprint('stock', __name__)


# Get the data from the https://api.nasdaq.com/api/
def get_data(symbol:str):   
    res = requests.get("https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks".format(symbol=symbol),headers={
"User-Agent" : "Mozilla/5.0"}).json()    
    
    return res

# # Get the data from the https://api.nasdaq.com/api/
def get_prices(shares): 
    share=[]
    for i in shares:       
        symbol = i['symbol']
        res = requests.get("https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/2021-07-22/2021-07-22?adjusted=true&sort=asc&limit=120&apiKey=pBHCmeSoVzoLK3G7R6AO1uMROS5prAf6".format(symbol=symbol),headers={"User-Agent" : "Mozilla/5.0"}).json()    
        share.append(res)
    # print(share)
    
    # for i in share:
    #     print(i['results'])
    return share

@stock.route('/share/', methods=['POST', 'PUT'])
@use_args({'symbol':fields.String(),'qty':fields.Integer() })
# Buy/Sell a number of shares of a certain stock via its symbol
def buy_shares(args:dict): 
    # Check if the symbol exist and get the data.
    get_symbol = get_data(args['symbol'])
    # Validate if the symbol is not None, if is None return a message with the error.
    if get_symbol['data'] is not None:    
        if request.method == 'POST': 
            # Buy share             
            if args['symbol'] == get_symbol['data']['symbol']:
                symbol= get_symbol['data']['symbol']
                qty=args['qty']  
                name = get_symbol['data']['companyName']
                price = get_symbol['data']['primaryData']['lastSalePrice']
                txn_amount = price * qty     
                
                txn = Transaction.query.filter_by(symbol=symbol).first()
                
                if txn is not None:
                    txn.qty += qty
                    db.session.commit()   
                else:    
                    new_tras= Transaction(symbol=symbol,name=name, qty=qty, last_price=txn_amount)
                    db.session.add(new_tras)
                    db.session.commit()
                return 'Successfully bought {qty} shares of company {name} by {price}'.format(qty=qty,name=name,price=price )
            else:
                return ('Buy Failed') 
            
        elif request.method == 'PUT':
            # Sell share
            get_symbol = get_data(args['symbol']) 
            if args['symbol'] == get_symbol['data']['symbol']:
                symbol= get_symbol['data']['symbol']
                qty=args['qty']  
                name = get_symbol['data']['companyName']        
                price = get_symbol['data']['primaryData']['lastSalePrice']       
                
                
                txn = Transaction.query.filter_by(symbol=symbol).first()
                
                qtyAvailable = db.session.query(db.func.sum(Transaction.qty)).filter(
                                                Transaction.symbol==symbol).first()[0]
                
                # Check if have enough shares to sell.
                if qty > qtyAvailable:            
                    return 'Not enough shares'        
                elif txn is not None:
                    txn.qty -= qty
                    db.session.commit() 
                    return 'Successfully sold {qty} shares of company {name} by {price}'.format(qty=qty,name=name,price=price )
                else:
                    return 'Error selling shares, check parameters'
            else:
                return ('Sell Failed.') 
    else: 
        return get_symbol

@stock.route('/list-shares', methods=['GET'])
# Get the list of shares owned
def list_shares():
    
    stock_schema = StockResponseSchema(many=True)
    all_stocks = db.session.query(Transaction).all()
    stocks = stock_schema.dumps(all_stocks)               
    shares = json.loads(stocks)   
       
    prueba = get_prices(shares)
    
    list_price = []
    for share in prueba:         
        list_price.append(share)
    # print(list_price)
    response = make_response(
                jsonify(
                    {"data": shares, "prices":list_price}, 
                ),
                200,
            )
    response.headers["Content-Type"] = "application/json"
    return response
    

@stock.route('/stock-prices', methods=['GET','POST'])
# Get the historic price of a stock you bought
def stock_price(args):
    
    return 'price'