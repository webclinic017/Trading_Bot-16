import backtrader
import datetime
from strategies import TestStrategy
data = backtrader.feeds.YahooFinanceCSVData(
    dataname='historicalData/tsla2021.csv',
    fromdate=datetime.datetime(2000, 1, 1),
    todate=datetime.datetime(2021, 12, 31), reverse=False)

cerebro = backtrader.Cerebro()
cerebro.broker.set_cash(1000000)
cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
cerebro.addsizer(backtrader.sizers.PercentSizer, percents = 99)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot(style="candlestick", barup='lawngreen', bardown='red')  