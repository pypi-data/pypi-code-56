import matplotlib.pyplot as plt


def ssimg(img, filename='', colorbar=False):
    plt.imshow(img)
    if colorbar:
        plt.colorbar()
    if filename: 
        plt.savefig(filename)
    else:
        plt.show()
    plt.close()


def plotxy(x, y, filename=''):
    plt.plot(x, y)
    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    plt.close()
