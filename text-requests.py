import I2C_LCD_driver
from time import *
#from coinmarketcap import Market
import time

# from fromurl.py
import urllib2, cookielib,requests
import json

eth_adress = "0x9c64Fd2804730683F3c5401aBA7285b2f33F3eDF"  # your ethereum address goes here
site = "https://etherchain.org/api/account/"
decimals = 2
final_site = site + eth_adress

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

lastreported = "https://api.nanopool.org/v1/eth/reportedhashrate/" + eth_adress
balance_nano = "https://api.nanopool.org/v1/eth/balance/" + eth_adress
priceusd = "https://api.coinmarketcap.com/v1/ticker/ethereum/"
#coinmarketcap = Market()
#price = coinmarketcap.ticker('Ethereum')

mylcd = I2C_LCD_driver.lcd()
# mylcd.lcd_display_string("HODL BOT 69000", 2)
# mylcd.lcd_display_string("HODL BOT 69000", 2)
req = requests.get(final_site, headers=hdr)

reqbal = requests.get(balance_nano, headers=hdr)
reqhashrate = requests.get(lastreported, headers=hdr)
reqprice = requests.get(priceusd, headers=hdr)
iteration = 0
while True:
    req = requests.get(final_site, headers=hdr)

    reqbal = requests.get(balance_nano, headers=hdr)
    reqhashrate = requests.get(lastreported, headers=hdr)
    reqprice = requests.get(priceusd, headers=hdr)
   # page = urllib2.urlopen(req)
    jsondata = req.json()
#    content = page.read()
 #   jsondata = json.loads(content)
  #  time.sleep(0.1)

    #pagehash = urllib2.urlopen(reqhashrate)
   # contenthash = pagehash.read()
    jsondatahash = reqbal.json()
  #  time.sleep(0.1)

   # pagebal = urllib2.urlopen(reqbal)
  #  contentbal = pagebal.read()
    jsondatabal = reqhashrate.json()
   # time.sleep(0.1)
    jsondatapriceusd = reqprice.json()





   # price = coinmarketcap.ticker('Ethereum')
    #	time.sleep(0.500)
   # price = str(int(round(float(price[price.find('price_usd') + 13:price.find('price_btc') - 13]))))
    price = round((float(jsondatapriceusd[0]['price_usd'])),1)
    final_price = str(price) + " " + str(round((float(jsondata['data'][0]['balance']) / 1000000000000000000), decimals)) + " " + str(round((float(jsondata['data'][0]['balance']) / 1000000000000000000), decimals) * float(price))
    nanostats = str(round(float(jsondatahash['data']),2)) + " " + str(round(float(jsondatabal['data']), 2))
    print(final_price)
    print(nanostats)
    iteration = iteration + 1
    print(iteration)
    mylcd.lcd_display_string(final_price, 1)
    mylcd.lcd_display_string(nanostats, 2)
  #  time.sleep(0.800)

