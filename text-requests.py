#2C_LCD_driver.py is needed https://gist.github.com/vay3t/8b0577acfdb27a78101ed16dd78ecba1
#put it in the same folder                                                                        
#add your ethereum address to eth_adress
#donate to 0x9c64Fd2804730683F3c5401aBA7285b2f33F3eDF or not , I'll live
import I2C_LCD_driver
from time import *
import time
import requests
import json
from requests.exceptions import ConnectionError
eth_address = ""  # your ethereum address goes here
site = "https://etherchain.org/api/account/"
decimals = 2
final_site = site + eth_address

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

lastreported = "https://api.nanopool.org/v1/eth/reportedhashrate/" + eth_address
balance_nano = "https://api.nanopool.org/v1/eth/balance/" + eth_address
priceusd = "https://api.coinmarketcap.com/v1/ticker/ethereum/"
mylcd = I2C_LCD_driver.lcd()
req = requests.get(final_site, headers=hdr)
reqbal = requests.get(balance_nano, headers=hdr)
reqhashrate = requests.get(lastreported, headers=hdr)
reqprice = requests.get(priceusd, headers=hdr)
iteration = 0
while True:
    try:
        req = requests.get(final_site, headers=hdr)
    except requests.exceptions.ConnectionError as e:   
        print e
        req = "No response"
    while type(req) == str:
	    req = requests.get(final_site, headers=hdr)
            if type(req) != str:
                break
    try:
        reqbal = requests.get(balance_nano, headers=hdr)
    except requests.exceptions.ConnectionError as e: 			#nanopool stuff 
        print e
        reqbal = "No response"
    while type(reqbal) == str:
	    reqbal = requests.get(balance_nano, headers=hdr)
            if type(reqbal) != str:
                break
    try:
        reqhashrate = requests.get(lastreported, headers=hdr)
    except requests.exceptions.ConnectionError as e:       #hashrate for nanopool leave it and if you don't mine it will show nothing on the second row of the LCD or show 0's
        print e
        reqhashrate = "No response"

    while type(reqhashrate) == str:
        reqhashrate = requests.get(lastreported, headers=hdr)
        if type(reqhashrate) != str:
                break


    try:
        reqprice = requests.get(priceusd, headers=hdr)
    except requests.exceptions.ConnectionError as e:  
        print e
        reqprice = "No response"
    while type(reqprice) == str:
        reqprice = requests.get(priceusd, headers=hdr)
        if type(reqprice) != str:
            break

    jsondata = req.json()
    jsondatahash = reqbal.json()
    jsondatabal = reqhashrate.json()
    jsondatapriceusd = reqprice.json()
    price = round((float(jsondatapriceusd[0]['price_usd'])),1)

    if price >= 1000:
	nanostats = "LAMBO ALERT"
    final_price = str(price) + " " + str(round((float(jsondata['data'][0]['balance']) / 1000000000000000000), decimals)) + " " + str(round((float(jsondata['data'][0]['balance']) / 1000000000000000000), decimals) * float(price))
    nanostats = str(round(float(jsondatahash['data']),2)) + " " + str(round(float(jsondatabal['data']), 2))
    iteration = iteration + 1
    mylcd.lcd_display_string(final_price, 1)
    mylcd.lcd_display_string(nanostats, 2)


