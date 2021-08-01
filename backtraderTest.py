import backtrader
import datetime
from strategies import TestStrategy

cerebro = backtrader.Cerebro()
cerebro.broker.set_cash(1000000)
# Create a Data Feed
data = backtrader.feeds.YahooFinanceCSVData(
    dataname='historicalData/BTC-USD2021.csv',
        # Do not pass values before this date
    fromdate=datetime.datetime(2021, 1, 8),
        # Do not pass values after this date
    todate=datetime.datetime(2021, 7, 31),
        reverse=False)

cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
cerebro.addsizer(backtrader.sizers.FixedSize, stake=20)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()