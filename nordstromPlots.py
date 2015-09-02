import nordstromDescStats as nds # see nordstromDescStats.py
import nordstromMachineLearning as nml # see nordstromMachineLearning.py
import pandas as pd

from bokeh.charts import Bar, show, output_notebook
from bokeh.plotting import figure, show, ColumnDataSource, Legend
from bokeh.models import HoverTool
from bokeh.io import gridplot

output_notebook()

class nordstromPlots():
    def __init__(self):
        #import data munging tools
        self.menCsv = pd.DataFrame.from_csv('nM.csv')
        self.womenCsv = pd.DataFrame.from_csv('nW.csv')

        self.menStats = nds.descriptiveStats(self.menCsv)
        self.womenStats = nds.descriptiveStats(self.womenCsv)

        self.menPlot = nds.plotPrep(self.menCsv)
        self.womenPlot = nds.plotPrep(self.womenCsv)

        self.menColors = nds.colorReduce(self.menCsv).pdDF
        self.womenColors = nds.colorReduce(self.womenCsv).pdDF
        self.mColorPrep = nds.colorDataPrep(self.menColors)
        self.wColorPrep = nds.colorDataPrep(self.womenColors)

    def nTermsCounted(self):
        mdBar = Bar(
            {'men':self.menStats.summary.values(),'women':self.womenStats.summary.values()},
            cat=self.menStats.summary.keys(),
            legend=True,
            width=450,height=450,
            xlabel='Term Groups',ylabel="Terms Counted",
            )
        return(mdBar)

    def nUniqueTermsCounted(self):
        mduBar = Bar(
            {'men':self.menStats.uniqueSummary.values(),'women':self.womenStats.uniqueSummary.values()},
            cat=self.menStats.uniqueSummary.keys(),
            legend=True,
            width=450,height=450,
            xlabel='Term Groups',ylabel="Unique Terms",
            )
        return(mduBar)

    def ratioPlot(self):
        ratioInit = nds.ratioAnalysis(self.menStats,self.womenStats)
        ratioData = ratioInit.ratioData

        hover = HoverTool(
            tooltips = [
                ("ratio","@ratio"),
                ("", "@desc"),
            ]
        )

        ratioPlot = figure(plot_width=450, plot_height=450,tools=[hover])
        ratioSource = ColumnDataSource(
        data=dict(
            x=ratioData['x'],
            y=ratioData['y'],
            desc=ratioData['desc'],
            ratio=ratioData['ratio']
            )
        )
        ratioPlot.scatter(
            'x', 'y',
            size=10,
            fill_color=[
                '#F4C2C2','#FF0000','#D73B3E','#800000',
                '#98FB98','#03C03C','#008000','#006400'
            ],
            source=ratioSource,line_color=None,tools=[hover]
        )

        show(ratioPlot)

    def itemBarPlot(self):
        itemBar = Bar(
            {'men':self.menPlot.itemZip.values(),'women':self.womenPlot.itemZip.values()},
            cat=self.menPlot.itemZip.keys(),
            legend=True,title="Items",
            width=900,height=450,
            xlabel='Items',ylabel="Count",
            tools=None
            )
        show(itemBar)

    def patternBarPlot(self):
        patternBar = Bar(
            {'men':self.menPlot.patternZip.values(),'women':self.womenPlot.patternZip.values()},
            cat=self.menPlot.patternZip.keys(),
            legend=True,title="Patterns",
            width=450,height=450,
            xlabel='Patterns',ylabel="Count",
            tools=None
            )
        return(patternBar)

    def fitBarPlot(self):
        fitBar = Bar(
            {'men':self.menPlot.fitZip.values(),'women':self.womenPlot.fitZip.values()},
            cat=self.menPlot.fitZip.keys(),
            legend=True,title="Fits",
            width=450,height=450,
            xlabel='Fits',ylabel="Count",
            )
        return(fitBar)

    def textureBarPlot(self):
        textureBar = Bar(
            {'men':self.menPlot.textureZip.values(),'women':self.womenPlot.textureZip.values()},
            cat=self.menPlot.textureZip.keys(),
            legend=True,title="Textures",
            width=450,height=450,
            xlabel='Textures',ylabel="Count",
            )
        return(textureBar)

    def colorBarPlot(self):
        colorBP = Bar(
            {'men':self.mColorPrep.freqTable.values(),'women':self.wColorPrep.freqTable.values()},
            cat=self.mColorPrep.freqTable.keys(),
            legend=True,title='Colors',
            width=450,height=450,
            xlabel='Colors',ylabel="Count",
            )

        return(colorBP)

class pcaPlot(nml.pcaWrap):
    def __init__(self,df):
        self.pcDF = nml.preProcess(df)
        nml.pcaWrap.__init__(self,self.pcDF.redDup)

    def plot(self,title):
        cols = self.pcDF.columns.tolist()
        plot = figure(
            x_axis_label = cols[0],
            y_axis_label = cols[1],
            plot_width = 450,plot_height = 450,
            title=title,
            )
        plot.scatter(
            self.norm_pcDF[cols[0]].tolist(),self.norm_pcDF[cols[1]].tolist(),
            )
        return(plot)
