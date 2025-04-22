class OrderStatus:
    def __init__(self, data, quantity):
        self.data = data
        self.marketPosition = 0
        self.buyPrice = 0
        self.sellPrice = 0
        self.netPnl = 0
        self.netPnlList = [0]
        self.quantity = quantity

    def Buy(self, orderType, orderPrice):
        if orderType.lower().strip() == "market":
            buyPrice = orderPrice
            self.marketPosition += self.quantity
        elif orderType.lower().strip() == "limit":
            if orderPrice > self.data[len(self.data)-1][3]:
                return "Order failed. Limit buy price must be below current close."
            else:
                buyPrice = orderPrice
        self.buyPrice = buyPrice
        if self.marketPosition == 0:
            self.CalculatePnl(self.buyPrice, self.sellPrice)
        return buyPrice
    
    def Sell(self, orderType, orderPrice):
        if orderType.lower().strip() == "market":
            sellPrice = orderPrice
            self.marketPosition -= self.quantity
        elif orderType.lower().strip() == "limit":
            if orderPrice < self.data[len(self.data)-1][3]:
                return "Order failed. Limit sell price must be above current close."
            else:
                sellPrice = orderPrice
        self.sellPrice = sellPrice
        if self.marketPosition == 0:
            self.CalculatePnl(self.buyPrice, self.sellPrice)
        return sellPrice
    
    def CalculateUnrealized(self, buyPrice, currentPrice, buyOrderFilled=False):
        if buyOrderFilled:
            unrealized = currentPrice-buyPrice
            return unrealized
        else:
            return 0
    
    def CalculatePnl(self, buyPrice, sellPrice):
        self.netPnl += (sellPrice-buyPrice) * self.quantity
        self.netPnlList.append(self.netPnl)
        return sellPrice-buyPrice
        
    def SubmitOrder(self, status, orderType, speed, price):
        if speed.lower().strip() == "market":
            if orderType.lower().strip() == "buy":
                print(f"\nBuy order filled at {price}")
            elif orderType.lower().strip() == "sell":
                print(f"Sell order filled at {price}")
            return not status
        else:
            return status
