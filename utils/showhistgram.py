import matplotlib.pyplot as plt

def show_histgram(arr, x):
    plt.hist(arr, bins=x)
    plt.show()