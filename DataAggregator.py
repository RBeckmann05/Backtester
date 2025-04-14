class Aggregator:
    def __init__(self, data):
        self.data = data
    
    def AggregateData(self, aggregationPeriod):
        aggregatedData = {}
        barsCount = 0
        totalBars = len(self.data)//aggregationPeriod
        if len(self.data) % aggregationPeriod != 0:
            totalBars += 1
        for i in range(totalBars):
            open = self.data[i*aggregationPeriod][0]
            highestHigh = self.data[i*aggregationPeriod][1]
            lowestLow = self.data[i*aggregationPeriod][2]
            volume = 0
            for j in range(aggregationPeriod):
                if (i*aggregationPeriod + j) < len(self.data):
                    high = self.data[i*aggregationPeriod + j][1]
                    low = self.data[i*aggregationPeriod + j][2]
                    if high > highestHigh:
                        highestHigh = high
                    if low < lowestLow:
                        lowestLow = low
                    close = self.data[i*aggregationPeriod + j][3]
                    volume += self.data[i*aggregationPeriod + j][4]
            newBar = [open, highestHigh, lowestLow, close, volume]
            aggregatedData[barsCount] = newBar
            barsCount += 1
        return aggregatedData