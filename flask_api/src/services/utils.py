import requests
import datetime
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
    

# # Get the data from the https://api.polygon.io/v2/
def get_prices(shares): 
    share=[]
    today = datetime.date.today()
    today.strftime("%Y-%m-%d")
    yesterday = today - datetime.timedelta(days=1)    
    for i in shares:       
        symbol = i['symbol']
        res = requests.get("https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{yesterday}/{yesterday}?adjusted=true&sort=asc&limit=120&apiKey=pBHCmeSoVzoLK3G7R6AO1uMROS5prAf6".format(symbol=symbol, yesterday= yesterday),headers={"User-Agent" : "Mozilla/5.0"}).json()    
        share.append(res)
   
    return share

def get_prices_hour(shares): 
    share=[]
    today = datetime.date.today()
    today.strftime("%Y-%m-%d")
    yesterday = today - datetime.timedelta(days=1)    
    for i in shares:       
        symbol = i['symbol']
        res = requests.get("https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/hour/{yesterday}/{yesterday}?adjusted=true&sort=asc&limit=120&apiKey=pBHCmeSoVzoLK3G7R6AO1uMROS5prAf6".format(symbol=symbol, yesterday= yesterday),headers={"User-Agent" : "Mozilla/5.0"}).json()    
        share.append(res)
   
    return share

# Get the data from the https://api.nasdaq.com/api/
def get_data(symbol:str):   
    res = requests.get("https://api.nasdaq.com/api/quote/{symbol}/info?assetclass=stocks".format(symbol=symbol),headers={
"User-Agent" : "Mozilla/5.0"}).json()    
    
    return res