from BuySell import OrderStatus
from Indicators import Indicators
from DataAggregator import Aggregator
from PracticeData import ObtainData
from Randomizer import GetRandomData
from Charter import ChartData
import matplotlib.pyplot as plt

printDetails = True
plotDetails = True
plotChart = True

if __name__ == "__main__":
    #rawData = GetRandomData(10000, 10, 300, 2000)
    rawData = ObtainData(0, 9999)
    agg = Aggregator(rawData)
    data = agg.AggregateData(5)

    indicatorData = {}
    loadedBars = {}
    totalBars = len(data)
    netPnl = []
    netPnlTracker = [0]
    filled = False
    pnlChange = False
    orderCount = 0

    for i in range(totalBars):
        loadedBars[i] = data[i]
        order = OrderStatus(loadedBars)
        ind = Indicators(loadedBars)

        # Initialize Indicators Here
        sma = ind.SMA(50)
        atr = ind.ATR(10)
        fullSDV = ind.SDV(50, atr/2) # Volatility based multiplier for standard deviation
        sdvBelow = fullSDV[1]
        close = ind.Close(0)
        low = ind.Low(0)

        # Add Indicator Charting Data Here
        indList = [sma, sdvBelow, atr]
        indicatorData[i] = indList

        # Set Order Details Here
        buyOrderType = "market"
        sellOrderType = "market"
        buyPrice = 0
        sellPrice = 0

        # Strategy Logic Here
        if not filled and (low < sdvBelow) and (atr > 1): # Buy if price is deviating too much from mean and there is volatility
            buy = order.Buy(buyOrderType, buyPrice)
            filled = order.SubmitOrder(filled, "buy", buyOrderType, buy)
        if filled and (close > sma): # Sell after price returns to mean
            sell = order.Sell(sellOrderType, sellPrice)
            filled = order.SubmitOrder(filled, "sell", sellOrderType, sell)
            pnlChange = True
            orderCount += 1
        
        # Sell if in position and data ends
        if filled and (i == totalBars-1):
            sell = order.Sell(sellOrderType, sellPrice)
            filled = order.SubmitOrder(filled, "sell", sellOrderType, sell)
            pnlChange = True
            orderCount += 1

        # Backtest Prints Here
        if pnlChange:
            pnl = order.CalculatePnl(buy, sell)
            netPnl.append(pnl)
            netPnlTracker.append(sum(netPnl))
            if printDetails:
                print(f"Trade Pnl: ${round(pnl, 2)}")
                print(f"Net Pnl: ${round(sum(netPnl), 2)}")
                print(f"Order number: {orderCount}")
            pnlChange = False

    if plotDetails:
        plt.plot(netPnlTracker)
        plt.show()

    if plotChart:
        ChartData(data, True, indicatorData)
