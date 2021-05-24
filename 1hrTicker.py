import websocket, json, pprint, config, requests, numpy, talib
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET, tld='us')
exchange_info = client.get_exchange_info()

closes={}
for s in exchange_info['symbols']:
    closes[s['symbol']]=[]
print("Server Time:", exchange_info['serverTime'])
print("Time Zone:", exchange_info['timezone'])
print("Exchange Filters:", exchange_info['exchangeFilters'])
print("Rate Limits:")
pprint.pprint( exchange_info['rateLimits'])
print()

for symbol in closes:
    agg_trades = client.aggregate_trade_iter(symbol=symbol, start_str='1 hour ago UTC')
    agg_trade_list=[]
    for trade in agg_trades:
        agg_trade_list.append(trade["p"])
    if len(agg_trade_list) > 0:
        percent="{:.3%}".format((float(agg_trade_list[len(agg_trade_list)-1])-float(agg_trade_list[0]))/float(agg_trade_list[0]))
    print(percent, end=' ')
    print(symbol)