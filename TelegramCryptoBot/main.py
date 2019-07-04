from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
import json 

#Call api and grab coin info
#Send coin info to msg to be formatted 
def price(bot,update):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'id':'2764'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'db5a55e7-7cd4-4bf9-8ee1-f2e71239a70c',
        }

    session = Session()
    
    session.headers.update(headers)
    
    response = session.get(url, params=parameters)

    data = response.json()
    
    print(data['data']['2764']['name'])
    
    chat_id = update.message.chat_id
 
    #for element in data['data']:
    #    print(element)

    #print data["data"]["name"]
    #print(data)
    bot.sendMessage(chat_id,data)
    
#Initializes the telegram bot and listens for the /price command
def main():
    updater = Updater('886915510:AAHEIaXLNAFdmLDv6qHwotAAMv6ty_BQx7I')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('price',price))
    updater.start_polling()
    updater.idle()
    
    
if __name__ == '__main__':
    main()
        
        
