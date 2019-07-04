from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
import json 

#Call api and grab coin info
#Send coin info to msg to be formatted 
def price(bot,update):

    #Pull chat ID
    chat_id = update.message.chat_id
    

    symbol = input(bot.sendMessage(chat_id,"Please input a symbol"))
    
    print(symbol)
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol':symbol
    }
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

    #Price
    price = data['data'][symbol]['quote']['USD']['price']
    price = ('%.08f' % price)
    
    #Volume changes and marketcap
    vol24 = data['data'][symbol]['quote']['USD']['volume_24h']
    per1h = data['data'][symbol]['quote']['USD']['percent_change_1h']
    per24h = data['data'][symbol]['quote']['USD']['percent_change_24h']
    per7d = data['data'][symbol]['quote']['USD']['percent_change_7d']   
    mc = data['data'][symbol]['quote']['USD']['market_cap']

    #initialize array
    currencydata = [name,symbol,circ,total,rank,time,price,vol24,per1h,per24h,per7d,mc]
 
    #Post message locally
    print(currencydata)

    #Send message to bot
    bot.sendMessage(chat_id, currencydata)

#Initializes the telegram bot and listens for the /price command
def main():
    updater = Updater('886915510:AAHEIaXLNAFdmLDv6qHwotAAMv6ty_BQx7I')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('price',price,))
    updater.start_polling()
    updater.idle()
    
    
if __name__ == '__main__':
    main()
        
        
