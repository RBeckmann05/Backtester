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
    aggregationPeriod = 1
    quantity = 1
    printStatistics = False
    plotProfitChart = False
    plotBarChart = False

    # Ignore
    def __init__(self, data):
        self.data = data

    # Initialize indicators here:
    def IndicatorData(self):
        ind = Indicators(self.data)

        self.FSDV = ind.SDV(50, 1)
        self.sdvAbove = self.FSDV[0]
        self.sdvBelow = self.FSDV[1]
        self.sdv = self.FSDV[2]
        self.sma = ind.SMA(50)
        self.atr = ind.ATR(10)
        self.close = ind.Close(0)
        self.low = ind.Low(0)
        self.high = ind.High(0)
        belowSig = self.sdvBelow-self.atr
        aboveSig = self.sdvAbove+self.atr
        # If plotting indicators, add them here:
        return [aboveSig, belowSig, self.sma, aboveSig+self.sdv, belowSig-self.sdv]

    # Strategy Logic Here:
    def OnBarUpdate(self):
        belowSig = self.sdvBelow-self.atr
        aboveSig = self.sdvAbove+self.atr
        if order.marketPosition == 0: # If flat...
            if (self.low < belowSig): # If low of bar < standard deviation below mean...
                order.Buy("market", self.close) # Long at market
            elif (self.high > aboveSig): # If high of bar > standard deviation above mean...
                order.Sell("market", self.close) # Short at market

        elif order.marketPosition != 0: # If in positon...
            if (self.low < belowSig-self.sdv) and (order.marketPosition == 1):
                order.Buy("market", self.close)
            if (self.high > aboveSig+self.sdv) and (order.marketPosition == -1):
                order.Sell("market", self.close)

            while (self.close > self.sma) and (order.marketPosition > 0): # If return to mean...
                order.Sell("market", self.close) # Sell to cover at market
            while (self.close < self.sma) and (order.marketPosition < 0): # If return to mean...
                order.Buy("market", self.close) # Buy to cover at market


'''
Below is set logic, do not change unless adjusting:
-input data
'''


if __name__ == "__main__": # ADD ITERATION SYSTEM THAT ALSO PLOTS PROFIT DATA

    alphaList = []
    runCount = 20000
    for i in range(runCount):
        if runCount > 1:
            print(f"Iteration: {i}")
        # Input data here:
        data = GetRandomData(2000, 10, 1000, 8000, 4000)
        #rawData = GetRandomData(2000, 10, 1000, 8000, 4000) # Uncomment later
        #rawData = ObtainData(0, 9999)


        # Initializing variables/objects---
        #agg = Aggregator(rawData) # Uncomment later
        #data = agg.AggregateData(Strategy.aggregationPeriod) # Uncomment later
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
            order.loadedBars = i
            
        # Close position after data ends---
        while len(loadedBars) == totalBars and order.marketPosition != 0:
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
            #print(order.orderHistory)
        alphaList.append(stats[0])
        if runStrat.plotBarChart:
            ChartData(loadedBars, False, indicatorData, order.orderHistory)
        
    if runCount > 1:
        print(sum(alphaList)/len(alphaList))
        bins = list(range(-1700, 2300, 50))
        plt.hist(alphaList, bins=bins, edgecolor="black")
        plt.xticks(bins)
        plt.show()
