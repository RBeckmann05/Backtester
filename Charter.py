import matplotlib.pyplot as plt

def ChartData(data, printProgress=False, indicatorData={}, orderHistory={}):
    fig, ax = plt.subplots()
    for key, value in data.items():
        if printProgress:
            print(f"Charted Bar: {key}")
        plt.vlines(x=key, ymin=value[2], ymax=value[1], colors='black', lw=1)
        if value[3] > value[0]:
            plt.vlines(x=key, ymin=value[0], ymax=value[3], colors='green', lw=2)
        else:
            plt.vlines(x=key, ymin=value[3], ymax=value[0], colors='red', lw=2)
    if len(indicatorData) > 0:
        xList = []
        yList = []
        if printProgress:
            print("Plotting indicator data...")
        for i in range(len(indicatorData)):
            xList.append(i)
        for value in indicatorData.values():
            yList.append(value)
        ax.plot(xList, yList)
    if len(orderHistory) > 0:
        for key, value in orderHistory.items():
            if value[0].lower().strip() == "buy":
                plt.plot((key, key+2, key+1, key), (value[1]-2, value[1]-2, value[1]-1, value[1]-2), color="green")
                plt.fill((key, key+2, key+1, key), (value[1]-2, value[1]-2, value[1]-1, value[1]-2), color="green")
            elif value[0].lower().strip() == "sell":
                plt.plot((key, key+2, key+1, key), (value[1]+2, value[1]+2, value[1]+1, value[1]+2), color="red")
                plt.fill((key, key+2, key+1, key), (value[1]+2, value[1]+2, value[1]+1, value[1]+2), color="red")
    if printProgress:
        print("Chart loading...")
    plt.show()
