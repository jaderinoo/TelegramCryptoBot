from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from telegram.ext import (Updater, CommandHandler)
import json 
import time
import keys
import datetime

#Coinmarketcap based Crypto price bot
#Written by Jad El-Khatib 

currentDT = datetime.datetime.now()
cooldownSeconds = 0
#Finds the price for specified tokens
def price(bot,update):
    
    #Pull chat ID
    chat_id = update.message.chat_id
    
    #Temp set symbol until user input is implemented
    symbol = update.message.text
    
    #Format string and remove the /price and forces it to uppercase
    symbol = symbol.replace('/price ',"").upper()
    
    #Calls the coinmarketcap api with the chosen symbol
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol':symbol
    }
    
    #Unsafe but works well for testing
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': keys.cmcKey,
        }

    #Start session
    session = Session()
    
    #Set headers and pull response while pulling data
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data = json.loads(response.text)

    #Format the response and sets to a string
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
    message += 'Total Market cap: $' + str(mc) + '\n'
    message += '----------------------------------- \n'
    message += 'Price: $' + str(price) + '\n'
    message += 'volume-24H: $' + str(vol24) + '\n'
    message += 'Percentage Change-1H: ' + str(per1h) + '% \n'
    message += 'Percentage Change-24H: ' + str(per24h) + '% \n'
    message += 'Percentage Change-7D: ' + str(per7d) + '% \n'
    message += 'Time Updated: ' + time
  
    #Post message locally
    print(message)

    #Send message to bot
    bot.sendMessage(chat_id, message)
    currentDT = datetime.datetime.now()
    cooldown(cooldownSeconds,currentDT)
    return

#Finds the prices for the top 10 current cryptos
def top(bot,update): 
    
    #Pull chat ID
    chat_id = update.message.chat_id
    
    #Calls the coinmarketcap api with the chosen symbol
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'10',
        'convert':'USD'
    }
    
    #Unsafe but works well for testing
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': keys.cmcKey,
        }

    #Start session
    session = Session()
    
    #Set headers and pull response while pulling data
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data = json.loads(response.text)

    #Grab the initial values for item 0
    name = data['data'][0]['name']
    symbol = data['data'][0]['symbol']
    time = data['data'][0]['quote']['USD']['last_updated']
    price = data['data'][0]['quote']['USD']['price']
    
    #Format the price value to 2 decimals
    price = ('%.2f' % price)
    
    #Format the initial string for item 0
    message = '1: ' + name + ' (' + symbol + ') Price: $' + str(price) + '\n'
    
    #While loop to grab all remaining items
    i = 1
    while i < 10: #Count i up to 10 and add to message
        name = data['data'][i]['name']
        symbol = data['data'][i]['symbol']
        time = data['data'][i]['quote']['USD']['last_updated']
        price = data['data'][i]['quote']['USD']['price']
    
        #Format the price value to 2 decimals
        price = ('%.2f' % price)
        
        #Format the message
        message += str(i + 1) + ': ' + name + ' (' + symbol + ') Price: $' + str(price) + '\n'
        
        #increment 1 to move to next value
        i += 1
      
    #Add update time to strings    
    message += 'Time Updated: ' + time
    
    #Post message locally
    print(message)

    #Send message to bot
    bot.sendMessage(chat_id, message)
    currentDT = datetime.datetime.now()
    cooldown(cooldownSeconds,currentDT)
    return

#Pulls global statistics and sends it to the user
def market(bot,update):
    
    #Pull chat ID
    chat_id = update.message.chat_id
    
    url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
    parameters = {
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': keys.cmcKey,
    }
    
    #Start session
    session = Session()
    
    #Set headers and pull response while pulling data
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data = json.loads(response.text)

    #Grab the initial values for item 0
    btcdom = data['data']['btc_dominance']
    ethdom = data['data']['eth_dominance']
    active = data['data']['active_cryptocurrencies']
    totalmkt = data['data']['quote']['USD']['total_market_cap']
    total24h = data['data']['quote']['USD']['total_volume_24h']
    time = data['data']['quote']['USD']['last_updated']
    
    #Float formatting
    btcdom = ('%.2f' % btcdom)
    ethdom = ('%.2f' % ethdom)
    totalmkt = ('%.2f' % totalmkt)
    total24h = ('%.2f' % total24h)
    
    #Formatted string
    message = 'Total Market cap: $' + str(totalmkt) + '\n'
    message += 'Total 24h Volume: $' + str(total24h) + '\n'
    message += 'BTC Dominance: ' + str(btcdom) + '% \n'
    message += 'Eth Dominance: ' + str(ethdom) + '% \n'
    message += 'Total Active Currencies: ' + str(active) + '\n'
    message += 'Time Updated: ' + str(time) + '\n'
    
    #Post message locally
    print(message)

    #Send message to bot
    bot.sendMessage(chat_id, message)
    
    #Call main with a reset cooldown
    currentDT = datetime.datetime.now()
    cooldown(cooldownSeconds,currentDT)

    return

def help(bot,update): 

    #Pull chat ID
    chat_id = update.message.chat_id
        
    #Initialize message
    message = "Please dont spam the bot, it only has 333 requests a day :) \nA 20 second cooldown is placed after each command execution. \n \n" + "Current command list: \n" + "/Price (coin symbol) \n" + "/Top \n" + "/Market \n"+ "/Help \n"
    
    #Sends the help message to the user
    bot.sendMessage(chat_id, message)
    
    return
 
def cooldown(cooldownSeconds,currentDT):
    
    #Initialize the time in seconds needed to allow user input
    if cooldownSeconds == 0:
        cooldownSeconds = currentDT.second + 5
        print ("cc set to = " + str(currentDT.second))
        print ("Cooldown set to = " + str(cooldownSeconds))
       
    #Check if the initialized time is over 60, as the currentDT doesnt pass 60 
    if cooldownSeconds >= 60:
            cooldownSeconds = cooldownSeconds - 60
        
    #Continue to update currentDT until it matches the cooldown time
    while currentDT.second != cooldownSeconds:
        currentDT = datetime.datetime.now()
        time.sleep(1)
        print ("Current = " + str(currentDT.second))
        print ("Cooldown = " + str(cooldownSeconds))
 
#Initializes the telegram bot and listens for a command
def main():
    updater = Updater(keys.botKey)     
    dp = updater.dispatcher
    
    #Creating Handler
    dp.add_handler(CommandHandler('price',price))
    dp.add_handler(CommandHandler('top',top))
    dp.add_handler(CommandHandler('market',market))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler('start',help))
    
    #Start polling
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()



