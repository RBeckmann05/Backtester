import random

#data = {0 : [10, 11, 9, 10, 1000], # Bar number : open, high, low, close, volume
#        1 : [10, 12, 8, 10, 500]} 

def GetRandomData(barsCount=1000, volatility=2, volumeLow=300, volumeHigh=1500, ogClose=10):
    data = {}

    closePrice = ogClose

    for i in range(barsCount):
        # Simulate a small change
        openPrice = closePrice
        high = openPrice + random.uniform(0, volatility)
        low = openPrice - random.uniform(0, volatility)
        closePrice = random.uniform(low, high)
        volume = random.randint(volumeLow, volumeHigh)

        data[i] = [round(openPrice, 2), round(high, 2), round(low, 2), round(closePrice, 2), volume]

    return data
