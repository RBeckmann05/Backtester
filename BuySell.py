class OrderStatus:
    def __init__(self, data):
        self.data = data

    def Buy(self, orderType="market", orderPrice=0):
        if orderType.lower().strip() == "market":
            buyPrice = self.data[len(self.data)-1][3]
        elif orderType.lower().strip() == "limit":
            if orderPrice > self.data[len(self.data)-1][3]:
                return "Order failed. Limit buy price must be below current close."
            else:
                buyPrice = orderPrice
        return buyPrice
    
    def Sell(self, orderType="market", orderPrice=0):
        if orderType.lower().strip() == "market":
            sellPrice = self.data[len(self.data)-1][3]
        elif orderType.lower().strip() == "limit":
            if orderPrice < self.data[len(self.data)-1][3]:
                return "Order failed. Limit sell price must be above current close."
            else:
                sellPrice = orderPrice
        return sellPrice
    
    def CalculateUnrealized(self, buyPrice, currentPrice, buyOrderFilled=False):
        if buyOrderFilled:
            unrealized = currentPrice-buyPrice
            return unrealized
        else:
            return 0
    
    def CalculatePnl(self, buyPrice, sellPrice):
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
