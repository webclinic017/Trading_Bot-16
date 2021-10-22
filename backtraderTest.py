import backtrader
import datetime
from config import alpaca_paper
import alpaca_backtrader_api as Alpaca
from strategies import TestStrategy

ALPACA_KEY_ID = alpaca_paper['api_key']
ALPACA_SECRET_KEY = alpaca_paper['api_secret']
ALPACA_PAPER = True
fromdate=datetime.datetime(2021,1,1)
todate=datetime.datetime(2021,12,31)
tickers=['BTC-USD']
timeframes = {
    '1 Day':1440,
}

#data = backtrader.feeds.YahooFinanceData(
#    dataname='historicalData/btc-usd.csv',
#    fromdate=datetime.datetime(2000, 1, 1),
#    todate=datetime.datetime(2021, 12, 31), reverse=False)

cerebro = backtrader.Cerebro()
cerebro.broker.set_cash(1000000)
#cerebro.adddata(data)
cerebro.addstrategy(TestStrategy#, trailpercent=range(0,100), stoploss=range(0,100)
                    )
cerebro.addsizer(backtrader.sizers.PercentSizer, percents = 99)

store = Alpaca.AlpacaStore(
    key_id=ALPACA_KEY_ID,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER
)

if not ALPACA_PAPER:
    print(f"LIVE TRADING")
    broker = store.getbroker()
    cerebro.setbroker(broker)

DataFactory = store.getdata

for ticker in tickers:
    for timeframe, minutes in timeframes.items():
        print(f'Adding ticker {ticker} using {timeframe} timeframe at {minutes} minutes.')

        d = DataFactory(
            dataname=ticker,
            timeframe=backtrader.TimeFrame.Days,
            compression=1440,
            fromdate=fromdate,
            todate=todate,
            historical=True)

        cerebro.adddata(d)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot(style="candlestick", barup='lawngreen', bardown='red')  
