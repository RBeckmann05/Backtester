import math

class Indicators:
    def __init__(self, data):
        self.data = data

    # Returns open of a specified bar
    def Open(self, location):
        loc = len(self.data)-1-location
        return self.data[loc][0]
    
    # Returns high of a specified bar
    def High(self, location):
        loc = len(self.data)-1-location
        return self.data[loc][1]
    
    # Returns low of a specified bar
    def Low(self, location):
        loc = len(self.data)-1-location
        return self.data[loc][2]
    
    # Returns close of a specified bar
    def Close(self, location):
        loc = len(self.data)-1-location
        return self.data[loc][3]

    # Returns volume of a specified bar
    def Volume(self, location):
        loc = len(self.data)-1-location
        return self.data[loc][4]

    # Returns simple moving average
    def SMA(self, period):
        netSum = 0
        for i in range(min(period, len(self.data))):
            netSum += self.data[len(self.data)-(i+1)][3]
        return netSum / period
    
    # Returns average true range
    def ATR(self, period):
        atr = 0
        for i in range(min(period, len(self.data))):
            high = self.data[len(self.data)-(i+1)][1]
            low = self.data[len(self.data)-(i+1)][2]
            prevClose = self.data[len(self.data)-(i+1)][0]

            TR = max((high - low), abs(high - prevClose), abs(low - prevClose))
            atr += TR/period
        return atr
    
    # Returns volume weighted moving average
    def VWMA(self, period):
        closeList = []
        volSum = 0
        for i in range(min(period, len(self.data))):
            volSum += self.data[len(self.data)-(i+1)][4]
        volAvg = volSum/period
        for i in range(min(period, len(self.data))):
            volMult = round(self.data[len(self.data)-(i+1)][4]/volAvg)
            if volMult > 0:
                for j in range(volMult+1):
                    closeList.append(self.data[len(self.data)-(i+1)][3])
        return sum(closeList)/len(closeList)
    
    # Returns average volume per dollar using atr of specified bar
    def AVPD(self, location):
        loc = len(self.data)-(location+1)
        volume = self.data[loc][4]
        high = self.data[loc][1]
        low = self.data[loc][2]
        return volume / (high-low+1)
    
    # Returns a list of standard deviation uppper, lower, and regular
    def SDV(self, period, multiplier=1):
        n = period
        netSum = 0
        returnList = []
        sumForVar = 0
        for i in range(min(period, len(self.data))):
            netSum += self.data[len(self.data)-(i+1)][3]
        mean = netSum/period
        for i in range(min(period, len(self.data))):
            sumForVar += (self.data[len(self.data)-(i+1)][3]-mean)**2
        variance = sumForVar/n
        sdv = math.sqrt(variance)
        returnList.append(mean+(sdv*multiplier))
        returnList.append(mean-(sdv*multiplier))
        returnList.append(sdv)
        return returnList
