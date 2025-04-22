from BuySell import OrderStatus
from Indicators import Indicators
from DataAggregator import Aggregator
from PracticeData import ObtainData
from Randomizer import GetRandomData
from Charter import ChartData
from CalculateStats import Statistics
import matplotlib.pyplot as plt
'''
def Strategy(data):
    if order.marketPosition == 0:
        if (low < sdvBelow):
            order.Buy("market", close)
        elif (high > sdvAbove):
            order.Sell("market", close)

    elif order.marketPosition != 0:
        if (close > sma) and (order.marketPosition > 0):
            order.Sell("market", close)
        if (close < sma) and (order.marketPosition < 0):
            order.Buy("market", close)
    
    if i == totalBars-1 and order.marketPosition != 0:
        if order.marketPosition > 0:
            order.Sell("market", close)
        elif order.marketPosition < 0:
            order.Buy("market", close)
'''
    

if __name__ == "__main__":
    rawData = GetRandomData(20000, 10, 1000, 8000, 4000)
    #rawData = ObtainData(0, 9999)
    agg = Aggregator(rawData)
    data = agg.AggregateData(5)

    indicatorData = {}
    loadedBars = {}
    totalBars = len(data)
    order = OrderStatus(data)

    for i in range(totalBars):
        loadedBars[i] = data[i]
        ind = Indicators(loadedBars)

        FSDV = ind.SDV(50, 1.5)
        sdvAbove = FSDV[0]
        sdvBelow = FSDV[1]
        sma = ind.SMA(50)
        close = ind.Close(0)
        low = ind.Low(0)
        high = ind.High(0)
        if i > 50:
            indList = [sdvAbove, sdvBelow]   
        else:
            indList = [close, close, close]
        indicatorData[i] = indList


        quantity = 1

        if order.marketPosition == 0:
            if (low < sdvBelow):
                order.Buy("market", close)
            elif (high > sdvAbove):
                order.Sell("market", close)

        elif order.marketPosition != 0:
            if (close > sma) and (order.marketPosition > 0):
                order.Sell("market", close)
            if (close < sma) and (order.marketPosition < 0):
                order.Buy("market", close)
        
        if i == totalBars-1 and order.marketPosition != 0:
            if order.marketPosition > 0:
                order.Sell("market", close)
            elif order.marketPosition < 0:
                order.Buy("market", close)


    dataChange = loadedBars[len(loadedBars)-1][3] - loadedBars[0][3]
    alpha = order.netPnl - dataChange
    
    plt.plot(order.netPnlList)
    plt.show()
    ChartData(loadedBars, True, indicatorData)
    print(f"Alpha: ${round(alpha, 2)}")
    stats = Statistics()
    stats.GetAllStats(order.netPnlList, dataChange)

        