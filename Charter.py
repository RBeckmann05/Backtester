import matplotlib.pyplot as plt

def ChartData(data, printProgress=False):
    for key, value in data.items():
        if printProgress:
            print(f"Charted Bar: {key}")
        plt.vlines(x=key, ymin=value[2], ymax=value[1], colors='black', lw=1)
        if value[3] > value[0]:
            plt.vlines(x=key, ymin=value[0], ymax=value[3], colors='green', lw=2)
        else:
            plt.vlines(x=key, ymin=value[3], ymax=value[0], colors='red', lw=2)
    plt.show()
