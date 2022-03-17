from flask import Blueprint,request,jsonify,make_response
from services.schema.list import StockResponseSchema
from .app import db, Transaction
from webargs.flaskparser import use_args
from marshmallow import fields
import requests
import json
import datetime
# Init the Blueprints of be used in the stock routes.
stock = Blueprint('stock', __name__)

    #   Profit/Loss in percentage
def profit_loss_pct( price_bought, actual_price, symbol):        
    profit_loss_prcnt = (actual_price - price_bought)    
    if  actual_price == 0:       
        profit = symbol + " = " +  str(0) +"%" 
        return profit
    else:
        if profit_loss_prcnt < 0:
            loss = symbol+" = "+ str(round(profit_loss_prcnt*100/price_bought,2))+"%"           

            return loss
        else:        
            profit = symbol + " = " +  str(round(profit_loss_prcnt*100/price_bought,2)) +"%"            

            return profit
        
    
# Get the data from the https://api.nasdaq.com/api/
def get_data(symbol:str):   
    res = requests.get("https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks".format(symbol=symbol),headers={
"User-Agent" : "Mozilla/5.0"}).json()    
    
    return res

# # Get the data from the https://api.polygon.io/v2/
def get_prices(shares): 
    share=[]
    today = datetime.date.today()
    today.strftime("%Y-%m-%d")
    yesterday = today - datetime.timedelta(days=1)    
    for i in shares:       
        symbol = i['symbol']
        res = requests.get("https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/hour/{yesterday}/{yesterday}?adjusted=true&sort=asc&limit=120&apiKey=pBHCmeSoVzoLK3G7R6AO1uMROS5prAf6".format(symbol=symbol, yesterday= yesterday),headers={"User-Agent" : "Mozilla/5.0"}).json()    
        share.append(res)
   
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
    
    try:
        list_share = get_prices(shares)    
        list_price = []
        for i in list_share:         
            list_price.append(i)     
    except Exception:
        return 'Connection Error.(too many request to the api or internet down)'  
    
    ref_prices = []    
    for i in list_price:
        ref_prices.append(i['ticker']+ ' = '+ ' #Lowest= $' + str(i['results'][0]['l']) + ' #Highest= $' + str(i['results'][0]['h']) +' #Average= $' + str(round(i['results'][0]['vw'],2))) 
        
        
    share = []
    money = []    
    last_price = []
    profit = []
    
    cont = 0
    for i in shares:
        cont = cont + 1      
        # append to share list the symbol and price and  split the $ sign
        share.append(i['symbol'] +' : ' + i['last_price'])        
        splited = str(i['last_price']).split('$')
        
        # Convert str to float and  append to last_price list
        price_bought = float(splited[1])       
        last_price.append(price_bought)        
        
        # calculate Current value of the shares holding and append to money list
        sub_total = list_price[cont -1]['results'][0]['c']*i['qty']        
        money.append(i['symbol'] + ' = '+'$ '+ str(sub_total) + '   Qty: ' + str(i['qty']))   
        
        # calculate the profit and loss of shares and append to profit list     
        profit_loss = profit_loss_pct(price_bought,list_price[cont -1]['results'][0]['c'],i['symbol'])        

        profit.append(profit_loss)     
 
    response = make_response(
                jsonify(
                    {"data": shares, "value_shares":share,
                     'current_value_shares_holding': money,
                     "Profit/loss": profit,
                     "Current day reference prices:":ref_prices
                     }, 
                ),
                200,
            )
    response.headers["Content-Type"] = "application/json"
    return response
    

@stock.route('/stock-prices', methods=['GET'])
# Get the historic price of a stock you bought
def stock_price():
    
    stock_schema = StockResponseSchema(many=True)
    all_stocks = db.session.query(Transaction).all()
    stocks = stock_schema.dumps(all_stocks)               
    shares = json.loads(stocks) 
    list_share = get_prices(shares)
    
    list_price = []
    for share in list_share:         
        list_price.append(share)       
  
    response = make_response(
                jsonify(
                    { "prices":list_price}, 
                ),
                200,
            )
    response.headers["Content-Type"] = "application/json"
    return response