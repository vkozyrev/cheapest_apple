import os, urllib2, sys
from Cookie import *
from cookielib import *
sys.path.append("/home/vkozyrev/webapps/cheapest_apple")
os.environ['DJANGO_SETTINGS_MODULE'] = 'cheapest_apple.settings'

from cheapest_apple.cheapestapple.models import Box, Product, Price, Store
from django.db import models
from BeautifulSoup import BeautifulSoup

DEBUG = True
UPDATE = True

GOT_PRICE = 1
NO_PRICE = 0

def skimBH(url):
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        result = soup.find('span', {"class": "value"})
        result = result.contents[0].strip('$,')
        result = result.replace(',', '')
        result = float(result)
        return [GOT_PRICE, result]
    except:
        return [NO_PRICE, url]
    
def skimMacConnection(url):
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        result = soup.find('strong', {"id": "ctl00_Content_ucOrderInfo_price"})
        result = result.contents[0].strip('$,')
        result = result.replace(',', '')
        result = float(result)
        return [GOT_PRICE, result]
    except:
        return [NO_PRICE, url]

def skimMacMall(url):
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        try:
            result = soup.find('td', {"class": "infoPrice infoBorderContent wt15"})
            result = result.contents[0].strip('$,')
            result = result.replace(',', '')
            result = float(result)
            return [GOT_PRICE, result]
        except:
            try:
                result = soup.find('td', {"class": "infoContent infoPrice wt15"})
                result = result.contents[0].strip('$,')
                result = result.replace(',', '')
                result = float(result)
                return [GOT_PRICE, result]
            except:
                return [NO_PRICE, url]
    except:
        return [NO_PRICE, url]

def skimOnSale(url):
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        try:
            result = soup.find('td', {"class": "infoPrice infoBorderContent wt15"})
            result = result.contents[0].strip('$,')
            result = result.replace(',', '')
            result = float(result)
            return [GOT_PRICE, result]
        except:
            try:
                result = soup.find('td', {"class": "infoContent infoPrice wt15"})
                result = result.contents[0].strip('$,')
                result = result.replace(',', '')
                result = float(result)
                return [GOT_PRICE, result]
            except:
                return [NO_PRICE, url]
    except:
        return [NO_PRICE, url]

def skimJR(url):
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        try:
            result = soup.find('div', {"class": "productPriceValue"})
            result = result.contents[2].strip()
            result = result.strip('$,')
            result = result.replace(',', '')
            result = float(result)
            return [GOT_PRICE, result]
        except:
            try:
                result = soup.findAll('span', {'class': 'value'})
                result = result[0].contents[0].strip('$,')  
                result = result.replace(',', '')
                result = float(result)
                return [GOT_PRICE, result]
            except:
                return [NO_PRICE, url]
    except:
        return [NO_PRICE, url]

def skimAmazon(url):
    try:
        opener = urllib2.build_opener()
        # cookie from wireshark goes here
        opener.addheaders = [('Cookie', 'apn-user-id=c779ef2c-74d7-47e3-a028-cf7e3f9e97b2; UserPref=4lq2gWWfdpBMOQ3DmvOezdbis06qBawBwaj2HP5VlasV11Syun/ydFfPlL1wA7Y5VFwmr5tDAtaf5gDY0VW0Dyqb5yk51z+n5vR8SR1mWB5cQklMYdiNyCyf3NVGEgYOFUVuvkWzJB/LcClSlJhFBNYFbFcrE6jnYra5aQI6Va+4uyyicETHPZ44WOpSRLjKUfHtwkW46OJmGfw0ytEuLG92s2L6lD7tMDO6LKGzyj2ILsXm/BBq4Bl5wkAkcCpuHFqs6TvBYXX7VGAmogD+2kDY8w6u/rF68dfToYsoVehPsiEQveNkRDVDyLCQ70lPRSL5DTVasnqNORlCYy1lVh44aO/yBLAcvg6tVbqoeqLCphZMhc7steK/g8t4kRQPssBD9UZMLSDLhYiWV8sIT3YmxClJISSorksirIy4SoruW7jvOTtrK8BgdfvysnrA3PLfx9/e/l0=; session-token=\"7LBM1qSFWv2iYA8RAui1vxEt4xViQx2xK3ptkO7VrwMJLuYMm2wMZjLWh2MAzAsVrtEc5HJ0Y5TuF6NDCNQ1POATAOrbmoz0RRwNZ833gMxDSnZhHXw7tsNPcquUo0t/Bzo1wcqMikZ426x3jCW5ipLZjR1uBvH/h2I0N0K2dt1AXF4t7WHlsy4CpFZJbSdJhol6AkLVFVLqnqG9bLQ45ONJes+fOVy96Y+vVY7L+dfoAJb12NGsAVovAaJUsjlP+fB4AwXmzxQ=\"; x-main=uWbq4fHhBlAX8PYz5A1JfpCju97Blccb; ubid-main=189-8043320-1806639; session-id-time=2082787201l; session-id=180-1471901-9463168'),('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.231 Safari/534.10'),('Referer', 'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=Macbook&x=0&y=0')]
        page = opener.open(url)
        soup = BeautifulSoup(page)
        try:
            result = soup.find('b', {"class": "priceLarge"})
            result = result.contents[0].strip('$,')
            result = result.replace(',', '')
            result = float(result)
            return [GOT_PRICE, result]
        except:
            try:
                result = soup.findAll('span', {'class': 'price'})
                result = result[1].contents[0].strip('$,')  
                result = result.replace(',', '')
                result = float(result)
                return [GOT_PRICE, result]
            except:
                return [NO_PRICE, url]
    except:
        return [NO_PRICE, url]
    
functionMap = {"Amazon" : skimAmazon,
               "B&H": skimBH,
               "J&R": skimJR,
               "Mac Connection": skimMacConnection,
               "MacMall": skimMacMall,
               "onSale": skimOnSale}    

querySet = Price.objects.all()
for item in querySet:
    if DEBUG == True:
        print '<--------------------------------------------------->'
        print item.id
    url = item.link
    etailer = item.etailer
    oldPrice = item.price
    if DEBUG == True:
        print etailer.etailer
        querySet2 = item.product.all()
        for item2 in querySet2:
            print item2.title
        print "Old Price: " + str(oldPrice)
    newPrice = functionMap[str(etailer.etailer)](url)

    if newPrice[0] == NO_PRICE:
        if DEBUG == True:
            print "URL:       " + str(newPrice[1])
            print "URL NOT REACHABLE!"
    else:
        if newPrice[1] != oldPrice:
            if DEBUG == True:
                print "New Price: " + str(newPrice[1])
                print "UPDATE NEEDED!"
            if UPDATE == True:
                item.price = newPrice[1]
                item.save()
                print "UPDATED!"
        else:
            if DEBUG == True:
                print "New Price: " + str(newPrice[1])
                print "NO UPDATE NEEDED!"
    if DEBUG == True:
        print '<--------------------------------------------------->\n\n'
