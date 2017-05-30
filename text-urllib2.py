# _   _ ___________ _    ______ _____ _____ _____ _____ _____ _____ _____ 
#| | | |  _  |  _  \ |   | ___ \  _  |_   _|  _  |  _  |  _  |  _  |  _  |
#| |_| | | | | | | | |   | |_/ / | | | | | | |_| | |/' | |/' | |/' | |/' |
#|  _  | | | | | | | |   | ___ \ | | | | | \____ |  /| |  /| |  /| |  /| |
#| | | \ \_/ / |/ /| |___| |_/ | \_/ / | | .___/ | |_/ | |_/ | |_/ | |_/ /
#\_| |_/\___/|___/ \_____|____/ \___/  \_/ \____/ \___/ \___/ \___/ \___/ 
                                                                         
                                                                         


#donate to 0x9c64Fd2804730683F3c5401aBA7285b2f33F3eDF or not ill live
# I2C_LCD_driver.py is needed 



import I2C_LCD_driver
from time import *
from coinmarketcap import Market
import time

# from fromurl.py
import urllib2, cookielib
import json

eth_adress = ""  # your ethereum address goes here
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

coinmarketcap = Market()
price = coinmarketcap.ticker('Ethereum')

mylcd = I2C_LCD_driver.lcd()
# mylcd.lcd_display_string("HODL BOT 69000", 2)
# mylcd.lcd_display_string("HODL BOT 69000", 2)
req = urllib2.Request(final_site, headers=hdr)

reqbal = urllib2.Request(balance_nano, headers=hdr)
reqhashrate = urllib2.Request(lastreported, headers=hdr)

while True:

    try:
        page = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        page = urllib2.urlopen(req)
    content = page.read()
    jsondata = json.loads(content)
    time.sleep(0.1)

    try:
        pagehash = urllib2.urlopen(reqhashrate)
    except urllib2.HTTPError, e:
        pagehash = urllib2.urlopen(reqhashrate)
    contenthash = pagehash.read()
    jsondatahash = json.loads(contenthash)
    time.sleep(0.1)

    try:
        pagebal = urllib2.urlopen(reqbal)
    except urllib2.HTTPError, e:
        pagebal = urllib2.urlopen(reqbal)
    contentbal = pagebal.read()
    jsondatabal = json.loads(contentbal)
    time.sleep(0.1)

    price = coinmarketcap.ticker('Ethereum')
    #	time.sleep(0.500)
    price = str(int(round(float(price[price.find('price_usd') + 13:price.find('price_btc') - 13]))))
    final_price = str(price) + " " + str(
        round((float(jsondata['data'][0]['balance']) / 1000000000000000000), decimals)) + " " + str(
        round((float(jsondata['data'][0]['balance']) / 1000000000000000000), decimals) * float(price))
    nanostats = str(float(jsondatahash['data'])) + " " + str(round(float(jsondatabal['data']), 2))
    mylcd.lcd_display_string(final_price, 1)
    mylcd.lcd_display_string(nanostats, 2)
    time.sleep(0.800)

