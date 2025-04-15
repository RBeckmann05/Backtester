from BuySell import OrderStatus
from Indicators import Indicators
from DataAggregator import Aggregator
from PracticeData import ObtainData
from Randomizer import GetRandomData
from Charter import ChartData
import matplotlib.pyplot as plt

printDetails = True
plotDetails = False
plotChart = True

if __name__ == "__main__":
    #rawData = GetRandomData(10000, 300, 2000)
    rawData = ObtainData(0, 9999)
    agg = Aggregator(rawData)
    data = agg.AggregateData(5)

    loadedBars = {}
    totalBars = len(data)
    netPnl = []
    netPnlTracker = []
    filled = False
    pnlChange = False
    orderCount = 0

    for i in range(totalBars):
        loadedBars[i] = data[i]
        order = OrderStatus(loadedBars)
        ind = Indicators(loadedBars)

        # Initialize Indicators Here
        smaFast = ind.SMA(5)
        smaSlow = ind.SMA(10)
        atr = ind.ATR(5)

        # Set Order Details Here
        buyOrderType = "market"
        sellOrderType = "market"
        buyPrice = 0
        sellPrice = 0

        # Strategy Logic Here
        if not filled and (smaFast > smaSlow) and (atr > 1.5):
            buy = order.Buy(buyOrderType, buyPrice)
            filled = order.SubmitOrder(filled, "buy", buyOrderType, buy)
        if filled and (smaFast < smaSlow):
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
        ChartData(data, True)
