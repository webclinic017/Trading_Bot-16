import alpaca_backtrader_api
import backtrader as bt
from datetime import datetime

ALPACA_API_KEY = 'PKCX6SDJ0FULVDF5RQR4'
ALPACA_SECRET_KEY = 'l9nDUmQy1rx1r27YrMUCp3yKxSu6eP3NPuGfpR6d'
ALPACA_PAPER = True

class TestStrategy(bt.Strategy):

    params=(
            ('trailpercent', 0.0333),
            ('stoploss', 0.1333)
           )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.macd = bt.indicators.MACDHisto(self.data)
        self.ema = bt.indicators.ExponentialMovingAverage(self.data, period = 21)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECTUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))
            self.bar_executed = len(self)
        self.order = None

    def next(self):
        trailpercent=self.params.trailpercent
        stoploss=self.params.stoploss
        self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return
        if not self.position:
            if self.macd.macd[0] < self.macd.signal[0] and self.ema[0] > self.data[0]:
                    self.log('BUY LONG CREATED, %.2f' % self.dataclose[0])
                    self.order = self.buy()
            if self.macd.macd[0] > self.macd.signal[0] and self.ema[0] > self.data[0]:
                    self.log('SELL SHORT CREATED, %.2f' % self.dataclose[0])
                    self.order = self.sell()
        if self.position:
            if self.macd.macd[0] > self.macd.signal[0] and self.ema[0] < self.data[0] and self.getposition(data=self.data).size > 0:
                self.log('CLOSE LONG CREATED {}'.format(self.dataclose[0]))
                self.order = self.close(exectype=bt.Order.StopTrail, trailpercent=trailpercent)
            if self.macd.macd[0] < self.macd.signal[0] and self.ema[0] > self.data[0] and self.getposition(data=self.data).size < 0:
                self.log('CLOSE SHORT CREATED {}'.format(self.dataclose[0]))
                self.order = self.close(exectype=bt.Order.StopTrail, trailpercent=trailpercent)
            else:
                if self.getposition(data=self.data).size > 0:
                    if self.getposition(data=self.data).price - (self.getposition(data=self.data).price * stoploss) > self.data[0]:
                        self.order=self.close()
                if self.getposition(data=self.data).size < 0:
                    if self.getposition(data=self.data).price + (self.getposition(data=self.data).price * stoploss) < self.data[0]:
                        self.order=self.close()

cerebro = bt.Cerebro()
cerebro.addstrategy(TestStrategy)
cerebro.addsizer(bt.sizers.PercentSizer, percents = 99)

store = alpaca_backtrader_api.AlpacaStore(
    key_id=ALPACA_API_KEY,
    secret_key=ALPACA_SECRET_KEY,
    paper=ALPACA_PAPER)

if not ALPACA_PAPER:
  broker = store.getbroker()  # or just alpaca_backtrader_api.AlpacaBroker()
  cerebro.setbroker(broker)

DataFactory = store.getdata  # or use alpaca_backtrader_api.AlpacaData
data = DataFactory(dataname='BTC-USD', historical=True, fromdate=datetime(
    2021, 1, 1,0,0), timeframe=bt.TimeFrame.Days)
cerebro.adddata(data)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()