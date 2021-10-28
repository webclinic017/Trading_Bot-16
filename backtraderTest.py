import backtrader
import datetime
from config import alpaca_paper
import alpaca_backtrader_api 
from strategies import TestStrategy

data = backtrader.feeds.YahooFinanceData(
    dataname='historicalData/btc-usd.csv',
    fromdate=datetime.datetime(2000, 1, 1),
    todate=datetime.datetime(2021, 12, 31), reverse=False)

cerebro = backtrader.Cerebro()
cerebro.adddata(data)
cerebro.broker.set_cash(1000000)
cerebro.addstrategy(TestStrategy#, trailpercent=range(0,100), stoploss=range(0,100)
                                )
cerebro.addsizer(backtrader.sizers.PercentSizer, percents = 99)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot(style="candlestick", barup='lawngreen', bardown='red')  
