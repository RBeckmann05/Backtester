import math

class Statistics:
    def __init__(self, data={}):
        self.data = data

    def GetAllStats(self, tradeData, dataChange):
        returnList = []

        # Profit Data
        netProfit = tradeData[len(tradeData)-1]
        grossProfit = 0
        grossLoss = 0
        numWinners = 0
        numLosers = 0
        for i in range(1, len(tradeData)):
            if tradeData[i] > tradeData[i-1]:
                grossProfit += tradeData[i] - tradeData[i-1]
                numWinners += 1
            else:
                grossLoss += tradeData[i] - tradeData[i-1]
                numLosers += 1
        profitFactor = grossProfit / grossLoss
        returnList.append(netProfit)
        returnList.append(grossProfit)
        returnList.append(grossLoss)
        returnList.append(profitFactor)

        # Max Drawdown
        highestHigh = 0
        maxDD = 0
        for i in tradeData:
            highestHigh = max(highestHigh, i)
            dd = highestHigh - i
            maxDD = max(dd, maxDD)
        returnList.append(maxDD)

        # Sharpe Ratio
        n = len(tradeData)
        netSum = 0
        sumForVar = 0
        for i in range(n):
            netSum += tradeData[i]
        mean = netSum/n
        for i in range(n):
            sumForVar += (tradeData[i]-mean)**2
        variance = sumForVar/n
        sdv = math.sqrt(variance)
        sharpe = (netProfit - dataChange) / sdv
        returnList.append(sharpe)

        # Average winner/loser
        avgWinner = grossProfit / numWinners
        avgLoser = grossLoss / numLosers
        returnList.append(numWinners)
        returnList.append(numLosers)
        returnList.append(avgWinner)
        returnList.append(avgLoser)


        print(f"Total net profit: ${round(netProfit, 2)}")
        print(f"Gross profit: ${round(grossProfit, 2)}")
        print(f"Gross loss: ${round(grossLoss, 2)}")
        print(f"Profit factor: {round(profitFactor, 2)}")
        print(f"Max. drawdown: {round(maxDD, 2)}")
        print(f"Sharpe ratio: {round(sharpe, 2)}")
        print(f"Number winning trades: {numWinners}")
        print(f"Number losing trades: {numLosers}")
        print(f"Average winning trade: {round(avgWinner, 2)}")
        print(f"Average losing trade: {round(avgLoser, 2)}")
        return returnList

            
        '''
        Total net profit
        Gross profit
        Gross loss
        Profit factor
        Max. drawdown
        Sharpe ratio: (return-underlying return)/std returns
        Sortino ratio
        Ulcer index
        R squared
        Probability

        # trades
        Number Winners
        Number Losers
        Avg winning trade
        Avg losing trade

        '''