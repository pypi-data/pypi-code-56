import pandas as pd
from .datatools import options, HistogramList, Histogram

class TxtData(HistogramList):
    def __init__(self):
        self.__filenames = [x + " - data" for x in options.files if ".txt" in x]
        super().__init__([])    

        setValues = input("Manually set nIons/gfu for the histograms? \n(Default values set to 1, select y to change or any key to skip)\t y/n: ")
        if setValues == 'y':
            try:
                nIons = int(input("nIons: "))
            except:
                print("Error: enter a valid number for nIons!")
            try:
                gfu = float(input("gfu: "))
            except:
                print("Error: enter a valid number for gfu!")
        else:
            nIons = 1
            gfu = 1

        for filename in [x for x in options.files if ".txt" in x]:
            df = pd.read_csv(filename, delimiter="\t", header = None)
            df = df.loc[: len(df)/2]
            df.columns = ['x', 'y', 'y2', 'xy', 'x2y', 'n', 'w']

            histogram = Histogram(histname = filename.split(".txt")[0], filename = filename , df = df, nIons = nIons, gfu = gfu)
            self.addHistogram(histogram)

    #def __getNormalizationInfo(self):
    #    print("Getting information for normalization (pickle files loaded" )
    #    if not options.no_norm:
    #        for filename in self._filenames:
    #            self.normalize(filename)

    #def normalize(self, filename):
    #    print("-----------------------------")
    #    print("filename: {}".format(filename))
    #    while True:
    #        try:
    #            nIons = int(input("\tnIons: "))
    #            gfu = float(input("\tgun fluence unit: "))
    #            break
    #        except KeyboardInterrupt:
    #            return False
    #        except:
    #            print("ERROR: enter a valid value")
    #    for name, histogram in self.histogramsDict.items():
    #        if filename in name:
    #            histogram.normFactor = gfu * nIons
    #            histogram.normalize()
