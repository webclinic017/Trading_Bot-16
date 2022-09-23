import websocket, json, pprint, config, requests, numpy, talib, time
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

while True:
    for symbol in closes:
        agg_trades = client.aggregate_trade_iter(symbol=symbol, start_str='1 hour ago UTC')
        agg_trade_list=[]
        for trade in agg_trades:
            agg_trade_list.append(trade["p"])
        if len(agg_trade_list) > 0:
            percent="{:.3f}".format((float(agg_trade_list[len(agg_trade_list)-1])-float(agg_trade_list[0]))/float(agg_trade_list[0]))
        if symbol in closes:
            closes[symbol].append(percent)
        if symbol in closes:
            np_closes = numpy.array(closes[symbol], dtype=float)
            changeMovingAverage = talib.SMA(np_closes, timeperiod=2)
        print(percent, end='% ')
        print(symbol, end= ' ')
        print(changeMovingAverage, end=" ")
        if str(changeMovingAverage) == "[nan]":
            print()
        if float(percent) > float(changeMovingAverage):
            print("↑")
        if float(percent) < float(changeMovingAverage):
            print("↓")
        if float(percent) == float(changeMovingAverage):
            print("=")
        time.sleep(.1)