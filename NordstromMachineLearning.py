import nordstromDescStats as nds
import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
import random
from bokeh.plotting import show,figure,output_notebook

output_notebook()

class preProcess():

    def __init__(self,csv): #this can be waaay cleaner
        self.__df = pd.DataFrame.from_csv(csv)
        self.__extractItems = nds.itemReduce(self.__df)
        self.__redColors = nds.colorReduce(self.__extractItems.df)
        self.ordDF = nds.ordinate(self.__redColors,'0') # for now we are not using this second argument
        self.duplicate = self.ordDF.df
        self.redDup = self.duplicate.drop(['ItemName','VendorName','Color','sex','Price'],axis=1)

class datasetSplit():
    def __init__(self,df):
        self.df = df
        self.__dataSets()

    def __combine(self):
        pass

    def __testTrainSplit(self):
        numRecords = len(self.df)
        testNum = 0.25 * numRecords

        subset = []
        while (len(subset) < testNum):
            ind = random.randrange(numRecords)
            if ind not in subset:
                subset.append(ind)
            else:
                next

        return(subset)

    def __dataSets(self):
        subset = self.__testTrainSplit()
        self.test = self.df.loc[subset]
        self.test = self.test.reset_index(drop=True)

        trainSet = map(lambda x: x not in subset,range(len(self.df)))
        self.train = self.df.loc[trainSet]
        self.train = self.train.reset_index(drop=True)


class pcaWrap(datasetSplit):

    def __init__(self,df):
        self.df = df
        self.__comps = self.__pcaRun()
        self.pcDF = self.df[self.__maxExtract()]
        self.norm_pcDF = self.__normalize()


    def __pcaRun(self):
        aoa = self.df.as_matrix()
        clf = PCA(2)
        clf.fit(aoa)
        return(clf.components_)

    def __maxExtract(self):
        toExtract = []
        for i in self.__comps:
            mx = max(i.tolist())
            toExtract.append(i.tolist().index(mx))
        return(toExtract)

    def __normalize(self):
        normDF = self.pcDF
        for i in normDF.columns.tolist():
            mx = max(normDF[i].tolist())

            normDF[i] = map(lambda x: (float(normDF.loc[x,i]))/mx,normDF.index.tolist())
        return(normDF)

class pcaPlot(pcaWrap):

    def __init__(self,df):
        pcaWrap.__init__(self,df)

    def plot(self):
        cols = self.pcDF.columns.tolist()
        plot = figure(tools=[],
            x_axis_label = cols[0],
            y_axis_label = cols[1],
            )
        plot.scatter(self.norm_pcDF[cols[0]].tolist(),self.norm_pcDF[cols[1]].tolist())
        show(plot)
