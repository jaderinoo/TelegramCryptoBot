from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def get_url():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'5',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'db5a55e7-7cd4-4bf9-8ee1-f2e71239a70c',
        }
    

    return url
def price(url, headers, parameters):

    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
        
    data = json.loads(response.text)
    print(data)
    
def main():
    updater = Updater('886915510:AAHEIaXLNAFdmLDv6qHwotAAMv6ty_BQx7I')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('price',price))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()