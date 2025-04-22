from BuySell import OrderStatus
from Indicators import Indicators
from DataAggregator import Aggregator
from PracticeData import ObtainData
from Randomizer import GetRandomData
from Charter import ChartData
from CalculateStats import Statistics
import matplotlib.pyplot as plt


class Strategy():
    # Set aggregation period, order quantity, and print statements here:
    aggregationPeriod = 5
    quantity = 1
    printStatistics = True
    plotProfitChart = True
    plotBarChart = True

    # Ignore
    def __init__(self, data):
        self.data = data

    # Initialize indicators here:
    def IndicatorData(self):
        ind = Indicators(self.data)

        self.FSDV = ind.SDV(50, 1.5)
        self.sdvAbove = self.FSDV[0]
        self.sdvBelow = self.FSDV[1]
        self.sma = ind.SMA(50)
        self.close = ind.Close(0)
        self.low = ind.Low(0)
        self.high = ind.High(0)
        # If plotting indicators, add them here:
        return [self.sdvAbove, self.sdvBelow, self.sma]

    # Strategy Logic Here:
    def OnBarUpdate(self):
        if order.marketPosition == 0: # If flat...
            if (self.low < self.sdvBelow): # If low of bar < standard deviation below mean...
                order.Buy("market", self.close) # Long at market
            elif (self.high > self.sdvAbove): # If high of bar > standard deviation above mean...
                order.Sell("market", self.close) # Short at market

        elif order.marketPosition != 0: # If in positon...
            if (self.close > self.sma) and (order.marketPosition > 0): # If return to mean...
                order.Sell("market", self.close) # Sell to cover at market
            if (self.close < self.sma) and (order.marketPosition < 0): # If return to mean...
                order.Buy("market", self.close) # Buy to cover at market

    
'''
Below is set logic, do not change unless adjusting:
-input data
'''


if __name__ == "__main__":
    # Input data here:
    rawData = GetRandomData(20000, 10, 1000, 8000, 4000)
    #rawData = ObtainData(0, 9999)


    # Initializing variables/objects---
    agg = Aggregator(rawData)
    data = agg.AggregateData(Strategy.aggregationPeriod)
    indicatorData = {}
    loadedBars = {}
    totalBars = len(data)
    quantity = Strategy.quantity
    order = OrderStatus(data, quantity)

    # Bar updates here---
    for i in range(totalBars):
        loadedBars[i] = data[i]
        runStrat = Strategy(loadedBars)

        indList = runStrat.IndicatorData() 

        indicatorData[i] = indList

        runStrat.OnBarUpdate()

    # Close position after data ends---
    if i == totalBars-1 and order.marketPosition != 0:
        close = Indicators(loadedBars).Close(0)
        if order.marketPosition > 0:
            order.Sell("market", close)
        elif order.marketPosition < 0:
            order.Buy("market", close)

    dataChange = loadedBars[len(loadedBars)-1][3] - loadedBars[0][3]
    
    # Plot results---
    if runStrat.plotProfitChart:
        plt.plot(order.netPnlList)
        plt.show()
    if runStrat.plotBarChart:
        ChartData(loadedBars, True, indicatorData)
    runStats = Statistics()
    stats = runStats.GetAllStats(order.netPnlList, dataChange)
    if runStrat.printStatistics:
        print(f"Alpha: ${round(stats[0], 2)}")
        print(f"Total net profit: ${round(stats[1], 2)}")
        print(f"Gross profit: ${round(stats[2], 2)}")
        print(f"Gross loss: ${round(stats[3], 2)}")
        print(f"Profit factor: {round(stats[4], 2)}")
        print(f"Max. drawdown: $-{round(stats[5], 2)}")
        print(f"Sharpe ratio: {round(stats[6], 2)}")
        print(f"Number winning trades: {stats[7]}")
        print(f"Number losing trades: {stats[8]}")
        print(f"Average winning trade: ${round(stats[9], 2)}")
        print(f"Average losing trade: ${round(stats[10], 2)}")
        print(f"Average trade: ${round(stats[11], 2)}")

        
