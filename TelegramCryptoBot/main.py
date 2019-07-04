from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from telegram import (ForceReply)
from telegram.ext import (Updater, CommandHandler, MessageHandler)
import json 
import re

#Coinmarketcap based Crypto price bot
#Written by Jad El-Khatib 

def price(bot,update):

    #Initialize as BTC
    symbol = 'BTC'
    
    #Pull chat ID
    chat_id = update.message.chat_id
    
    #Temp set symbol until user input is implemented
    symbol = update.message.text
    
    #Format string and remove the /price and forces it to uppercase
    symbol = symbol.replace('/price ',"").upper()
    
    print(symbol)
    #Calls the coinmarketcap api with the chosen symbol
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol':symbol
    }
    
    #Unsafe but works well for testing
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'db5a55e7-7cd4-4bf9-8ee1-f2e71239a70c',
        }

    #Start session
    session = Session()
    
    #Set headers and pull response while pulling data
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data = json.loads(response.text)

    #Format the response and sets it to an array
    name = data['data'][symbol]['name']
    symbol = data['data'][symbol]['symbol']
    circ = data['data'][symbol]['circulating_supply']
    total = data['data'][symbol]['total_supply']
    rank = data['data'][symbol]['cmc_rank']
    time = data['data'][symbol]['last_updated']

    #Price volume changes and marketcap
    price = data['data'][symbol]['quote']['USD']['price']
    vol24 = data['data'][symbol]['quote']['USD']['volume_24h']
    per1h = data['data'][symbol]['quote']['USD']['percent_change_1h']
    per24h = data['data'][symbol]['quote']['USD']['percent_change_24h']
    per7d = data['data'][symbol]['quote']['USD']['percent_change_7d']   
    mc = data['data'][symbol]['quote']['USD']['market_cap']
    
    #Float formatting
    price = ('%.08f' % price)
    vol24 = ('%.2f' % vol24)
    per1h = ('%.3f' % per1h)
    per24h = ('%.3f' % per24h)
    per7d = ('%.3f' % per7d)
    mc = ('%.2f' % mc)

    #initialize array / Legacy method
    #currencydata = [name,symbol,circ,total,rank,time,price,vol24,per1h,per24h,per7d,mc]
 
    #Formatted string
    message = 'Name: ' + name + '\n'
    message += 'Symbol: ' + symbol + '\n' 
    message += 'CMC Rank: ' + str(rank) + '\n'
    message += 'Circulating Supply: ' + str(circ) + '\n'
    message += 'Total Supply: ' + str(total) + '\n'
    message += 'Total Market cap: ' + str(mc) + '\n'
    message += '----------------------------------- \n'
    message += 'Price: ' + str(price) + '\n'
    message += 'volume-24H: ' + str(vol24) + '\n'
    message += 'Percentage Change - 1H: ' + str(per1h) + '\n'
    message += 'Percentage Change - 24H: ' + str(per24h) + '\n'
    message += 'Percentage Change - 7D: ' + str(per7d) + '\n'
    message += 'Time Updated: ' + time + '\n'
  
    #Post message locally
    print(message)

    #Send message to bot
    bot.sendMessage(chat_id, message)

#Initializes the telegram bot and listens for the /price command
def main():
    updater = Updater('886915510:AAHEIaXLNAFdmLDv6qHwotAAMv6ty_BQx7I')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('price',price))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
        
        
