from flask import Blueprint,request,jsonify,make_response
from services.utils import profit_loss_pct, get_data, get_prices,get_prices_hour
from services.schema.list import StockResponseSchema
from .app import db, Transaction
from webargs.flaskparser import use_args
from marshmallow import fields
import json
from flasgger import swag_from




# Init the Blueprints of be used in the stock routes.
stock = Blueprint('stock', __name__)

@stock.route('/share', methods=['POST'])
@swag_from('./docs/stock/buy.yaml')
def buy_swagger():
    """Swagger help"""
    pass

@stock.route('/share', methods=['PUT'])
@swag_from('./docs/stock/sell.yaml')
def sell_swagger():
    """Swagger help"""
    pass

@stock.route('/share', methods=['POST', 'PUT'])
@use_args({'symbol':fields.String(),'qty':fields.Integer() })
# Buy/Sell a number of shares of a certain stock via its symbol
def buy_shares(args:dict): 
    # Check if the symbol exist and get the data.
    try:
        get_symbol = get_data(args['symbol'])
        symbol= get_symbol['data']['symbol']
        qty=args['qty']  
        name = get_symbol['data']['companyName']
        price = get_symbol['data']['primaryData']['lastSalePrice']           
        if request.method == 'POST': 
            #  If method if POST buy or add shares 
            
            txn = Transaction.query.filter_by(symbol=symbol).first()
            
            if txn is not None:
                txn.qty += qty
                db.session.commit()   
                return 'Successfully added {qty} shares of {symbol} by {price} per unit'.format(qty=qty,symbol=symbol,price=price )
            else:    
                new_tras= Transaction(symbol=symbol,name=name, qty=qty, last_price=price)
                db.session.add(new_tras)
                db.session.commit()
                return 'Successfully bought {qty} shares of {symbol} by {price} per unit '.format(qty=qty,symbol=symbol,price=price )
  
        elif request.method == 'PUT':    
             # If method if PUT buy or add shares                   
            txn = Transaction.query.filter_by(symbol=symbol).first()
            
            qtyAvailable = db.session.query(db.func.sum(Transaction.qty)).filter(
                                            Transaction.symbol==symbol).first()[0]
            
            # Check if have enough shares to sell.
            if qty > qtyAvailable:            
                return 'Not enough shares'
            # Sell shares and update the DB 
            elif txn is not None:
                txn.qty -= qty
                db.session.commit() 
                return 'Successfully sold {qty} shares of company {name} by {price}'.format(qty=qty,name=name,price=price )
            else:
                return 'Error selling shares, check parameters'
        else:
            return ('Sell Failed.') 
    except Exception: 
        return 'Connection Error.(too many request to the api or internet down)'


# Get the list of shares owned
@stock.route('/list-shares', methods=['GET'])
@swag_from('./docs/stock/stocks.yaml')
def list_shares():
    # Get forom the DB the data
    stock_schema = StockResponseSchema(many=True)
    all_stocks = db.session.query(Transaction).all()
    stocks = stock_schema.dumps(all_stocks)               
    shares = json.loads(stocks)  
    
    # Get current prices of shares
    try:
        list_share = get_prices(shares)    
        list_price = []
        for i in list_share:         
            list_price.append(i)     
    except Exception:
        return 'Connection Error.(too many request to the api or internet down)'
      
    # Formated lowest, highest and avg prices of the shares
    ref_prices = []    
    for i in list_price:
        ref_prices.append(i['ticker']+ ' = '+ ' #Lowest= $' + str(i['results'][0]['l']) + ' #Highest= $' + str(i['results'][0]['h']) +' #Average= $' + str(round(i['results'][0]['vw'],2))) 
        
        
    share = []
    money = []    
    last_price = []
    profit = []    
    cont = 0
    # Populating the data needed.
    for i in shares:
        cont = cont + 1      
        # append to share list the symbol and price and  split the $ sign
        share.append(i['symbol'] +' : ' + i['last_price'])        
        splited = str(i['last_price']).split('$')
        
        # Convert str to float and  append to last_price list
        price_bought = float(splited[1])       
        last_price.append(price_bought)        
        
        # Calculate Current value of the shares holding and append to money list
        sub_total = list_price[cont -1]['results'][0]['c']*i['qty']        
        money.append(i['symbol'] + ' = '+'$ '+ str(sub_total) + '   Qty: ' + str(i['qty']))   
        
        # Calculate the profit and loss of shares and append to profit list     
        profit_loss = profit_loss_pct(price_bought,list_price[cont -1]['results'][0]['c'],i['symbol'])        

        profit.append(profit_loss)     
 
    #  Custom Response to send the data.
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
@swag_from('./docs/stock/get_price.yaml')
# Get the historic price of a stock you bought
def stock_price():
    
    stock_schema = StockResponseSchema(many=True)
    all_stocks = db.session.query(Transaction).all()
    stocks = stock_schema.dumps(all_stocks)               
    shares = json.loads(stocks) 
    list_share = get_prices_hour(shares)
    
    list_price = []
    for share in list_share:         
        list_price.append(share)  
        
    # Formated lowest, highest and avg prices of the shares
    ref_prices = []    
    for i in list_price:
        ref_prices.append(i['ticker']+ ' = '+ ' #Lowest= $' + str(i['results'][0]['l']) + ' #Highest= $' + str(i['results'][0]['h']) +' #Average= $' + str(round(i['results'][0]['vw'],2))) 
             
  
    response = make_response(
                jsonify(
                    { "prices":ref_prices}, 
                ),
                200,
            )
    response.headers["Content-Type"] = "application/json"
    return response