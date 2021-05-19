import websocket, json, pprint, config, requests, numpy, talib
from binance.client import Client

symbol="btcusdt"
type="@kline_"
interval="15m"
stream = symbol + type + interval
query = "/api/v3/ticker/24hr"
baseurl = "https://api.binance.com"    
url = baseurl+query
request = requests.get(url)
#pprint.pprint(request.json())

client = Client(config.API_KEY, config.API_SECRET, tld='us')
time_res = client.get_server_time()
#status = client.get_system_status()
exchange_info = client.get_exchange_info()
closes={}
for s in exchange_info['symbols']:
    closes[s['symbol']]=[]
print(time_res)

def on_open(ws):
    print("opened connection")
def on_close(ws):
    print("closed connection")
def on_message(ws, message):
    print("recieved message")
    json_message = json.loads(message)
    changeDict={}
    counter=0
    for y in range(len(json_message)):
        changeDict[json_message[counter]['P']] = json_message[counter]['s']
        counter+=1
    int_changeDict = {float(k) : v for k, v in changeDict.items()}
    for change, symbol in sorted(int_changeDict.items()): 
        if symbol in closes:
             closes[symbol].append(change)
        print(change, symbol, end = ' ')
        if symbol in closes:
            np_closes = numpy.array(closes[symbol])
            changeMovingAverage = talib.SMA(np_closes, timeperiod=30)
            last_changeMovingAverage = changeMovingAverage[-1]
            formatted = "{:.3f}".format(last_changeMovingAverage)
            print(formatted, end = ' ')
        if formatted == "nan":
            print()
        if change > float(formatted):
            print("↑")
        if change < float(formatted):
            print("↓")
        if change == float(formatted):
            print("=")
ws = websocket.WebSocketApp("wss://stream.binance.us:9443/ws/!ticker@arr", on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()