import backtrader

class TestStrategy(backtrader.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.macd = backtrader.indicators.MACDHisto(self.data)
        #self.rsi = backtrader.indicators.RelativeStrengthIndex(self.data)
        #self.bbands = backtrader.indicators.BollingerBands(self.data)
        #self.psar = backtrader.indicators.ParabolicSAR(self.data)
        self.ema = backtrader.indicators.ExponentialMovingAverage(self.data, period = 21)

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
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return
        if not self.position:
            if self.macd.macd[0] < self.macd.signal[0] and self.ema[0] > self.data[0]:
                    self.log('BUY CREATED, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        if self.position:
            if self.macd.macd[0] > self.macd.signal[0] and self.ema[0] < self.data[0]:
                self.log('SELL CREATED {}'.format(self.dataclose[0]))
                self.order = self.sell()