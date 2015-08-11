import nordstromDescStats as nds
import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
from math import sqrt
from random import sample


class preProcess():

    def __init__(self,csv): #this can be waaay cleaner
        self.__df = pd.DataFrame.from_csv(csv)
        self.__extractItems = nds.itemReduce(self.__df)
        self.__redColors = nds.colorReduce(self.__extractItems.df)
        self.ordDF = nds.ordinate(self.__redColors)
        self.duplicate = self.ordDF.df
        self.redDup = self.duplicate.drop(['ItemName','VendorName','Color','Price'],axis=1)

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

class dispersal:
    # returns a score that measures the dispersal/spread of a dataset
    def __init__(self,df):
        self.df = df
        self.dispersal = self.__averageSpread()

    def __spread(self):
        indexes = self.df.index.tolist()
        data = {
            'total':0,
            'count':0
            }
        for a in indexes:
            p1 = self.df.loc[int(a)].tolist()
            for b in indexes:
                p2 = self.df.loc[int(b)].tolist()
                result = sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
                data['total']+=result
                data['count']+=1

        avgDist = data['total']/data['count']
        return avgDist

    def __averageSpread(self):
        for i in self.df.columns.tolist():
            self.df = self.df[self.df[i] != 0.]
        self.df.reset_index(drop=True,inplace=True)
        indexes = self.df.index.tolist()
        samp = sample(indexes,100)
        self.df.iloc[samp]
        return self.__spread()
