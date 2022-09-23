import json, pprint, requests, time
from binance.client import Client

botType = input('[A]rithmetic or [G]eometric:')
upperBound = input('Upper Bound:')
lowerBound = input('Lower Bound:')
grids = input('Number of Grids:')

run = True
while (run):
    symbol="BTCUSD"
    query = "/api/v3/ticker/price?symbol="
    baseurl = "https://api.binance.us"    
    url = baseurl+query+symbol
    request = requests.get(url)
    pprint.pprint(request.json())
    time.sleep(1)
