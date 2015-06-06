from collections import OrderedDict
import re

class Props:
    
    def __init__(self):
        self.items = self.__pieces()
        self.fits = self.__fits()
        self.patterns = self.__patterns()
        self.textures = self.__textures()
        
    def __pieces(self):
    #list of all the pieces we may want to look for in either collection
        return(
            [
                'Shirt','Polo','Shorts','Jacket','Jeans','Pants',
                'Trunks','Hoodie','Sweater','Sweatshirt','Trousers',
                'Pullover','Jersey','Top','Coat','Tank',
                'Jogger','Suit','Blazer','Vest','Chinos',
                'Tank','Tee','Cardigan','Bikini',
                'Skirt','Tunic','Gown','Blouse','Camisole',
                'Leggings','Bottoms','Tights','Jumpsuit',
                'Romper','Shell','Swimsuit','Pajamas','Blouson',
                'Capri','Shirtdress','Chemise','Bodysuit','Nightgown',
                'Panties','Slipdress'
                #eliminated Dress for now
            ]
        )
    
    def __fits(self):
    #list of all the fits we may want to look for in either collection
        return(
            [
                'Trim','Slim','Regular','Straight','Stretch',
                'Modern','Tailored','Relaxed','Skinny',
                'Slouchy','Crop','Boyfriend','Wide',
                'Boxy','Oversize','Bootcut'
            ]
        )
        
    def __patterns(self):
    #list of all the patterns we may want to look for in either collection
        return(
            [
                'Stripe','Plaid','Graphic','Colorblock','Floral',
                'Houndstooth','Indigo','Contrast','Print','Lace',
                'Woven','Crochet','Quilted','Colored','Metallic',
                'Chevron'
            ]
        )
    
    def __textures(self):
    #list of all the textures we may want to look for in either collection
        return(
            [
                'Nylon','Textured','Cotton','Wool','Linen',
                'Woven','Silk','Twill','Knit','Microfiber',
                'Wrinkle','Jacquard','Mesh','Leather','Gingham',
                'Cashmere','Herringbone','Houndstooth','Fleece','Lace',
                'Chiffon','Crochet','Quilted','Crepe','Distressed',
                'Textured','Ruffled','Crinkled','Fur','Slub'
            ]
        )
    
class dfExtract(Props):
    
    def __init__(self,df):
        Props.__init__(self)
        self.df = df
        self.itemFreqTable = self.__itemFreqTable()
        self.ItemFreqCnt = self.__itemFreqCount()
        self.FitFreqCnt = self.__fitFreqCount()
        self.PatternFreqCnt = self.__patternFreqCount()
        self.TextureFreqCnt = self.__textureFreqCount()
        
    def __itemFreqTable(self):
    #creates a table of frequency for all of the item names
        itemNames = self.df['ItemName']
        terms = (' '.join(itemNames.tolist())).split(' ')
        
        freqTable = {}
        for term in terms:
            freqTable[term] = freqTable.get(term,0)+1
     
        return(freqTable)
    
    def __itemFreqCount(self):
    #returns the counts of ONLY the selected items
        itemCounts = []
        for item in self.items:
            itemCounts.append(self.itemFreqTable.get(item))
        return(itemCounts)
    
    def __fitFreqCount(self):
    #returns the counts of ONLY the selected fits
        fitCounts = []
        for fit in self.fits:
            fitCounts.append(self.itemFreqTable.get(fit))
        return(fitCounts)
    
    def __textureFreqCount(self):
    #returns the counts of ONLY the selected textures
        textureCounts = []
        for texture in self.textures:
            textureCounts.append(self.itemFreqTable.get(texture))
        return(textureCounts)
    
    def __patternFreqCount(self):
    #returns the counts of ONLY the selected patterns
        patternCounts = []
        for pattern in self.patterns:
            patternCounts.append(self.itemFreqTable.get(pattern))
        return(patternCounts)

    
class descriptiveStats(Props):
    
    def __init__(self,df):
        self.data = dfExtract(df)
        self.tFits = self.__totalFits()
        self.tTextures = self.__totalTextures()
        self.tItems = self.__totalItems()
        self.tPatterns = self.__totalPatterns()
    
        self.summary = self.summary()
        self.uniqueSummary = self.uniqueSummary()
        
    def __superSum(self,array):
    #Temporary solution; this skips things that will muck up our totals
        total = 0
        for i in array:
            try:
                total += i
            except:
                next
        return(total) 
    
    
    def __totalFits(self):
    #total number of fits counted
        return(self.__superSum(self.data.FitFreqCnt))
        
    def __totalTextures(self):
    #total number of textures counted
        return(self.__superSum(self.data.TextureFreqCnt))
    
            
    def __totalItems(self):
    #total number of items counted
        return(self.__superSum(self.data.ItemFreqCnt))
    
    def __totalPatterns(self):
    #total number of patterns counted
        return(self.__superSum(self.data.PatternFreqCnt))
    
    def summary(self):
    #returns summary of the total counts for the dataset
        return(
            {
                'Fits':self.tFits,
                'Textures':self.tTextures,
                'Items':self.tItems,
                'Patterns':self.tPatterns
            }
        )
    
    def uniqueSummary(self):
    #returns summary of the total unique counts for the dataset
        return(
            {
                'Fits':len(filter(None,self.data.FitFreqCnt)),
                'Textures':len(filter(None,self.data.TextureFreqCnt)),
                'Items':len(filter(None,self.data.ItemFreqCnt)),
                'Patterns':len(filter(None,self.data.PatternFreqCnt))
            }
        )
        
class plotPrep(Props):
    
    def __init__(self,df):
        Props.__init__(self)
        self.data = dfExtract(df)
        self.fitZip = self.__fitZip()
        self.itemZip = self.__itemZip()
        self.textureZip = self.__textureZip()
        self.patternZip = self.__patternZip()
    
    def __fitZip(self):
    #combines select fit data
        newDict = {}
        for i in range(1,(len(self.fits))):
            s = [self.fits[i],self.data.FitFreqCnt[i]]
            newDict[self.fits[i]] = self.data.FitFreqCnt[i]

        for i in newDict.keys():
            if newDict[i] == None:
                newDict[i] = 0

        sortedDict = OrderedDict(sorted(newDict.items(),key=lambda t:t[0]))
        return(sortedDict)
    
    def __itemZip(self):
    #combines select item data
        newDict = {}
        for i in range(1,(len(self.items))):
            s = [self.items[i],self.data.ItemFreqCnt[i]]
            newDict[self.items[i]] = self.data.ItemFreqCnt[i]

        for i in newDict.keys():
            if newDict[i] == None:
                newDict[i] = 0

        sortedDict = OrderedDict(sorted(newDict.items(),key=lambda t:t[0]))
        return(sortedDict)
    
    def __textureZip(self):
    #combines select texture data
        newDict = {}
        for i in range(1,(len(self.textures))):
            s = [self.textures[i],self.data.TextureFreqCnt[i]]
            newDict[self.textures[i]] = self.data.TextureFreqCnt[i]

        for i in newDict.keys():
            if newDict[i] == None:
                newDict[i] = 0

        sortedDict = OrderedDict(sorted(newDict.items(),key=lambda t:t[0]))
        return(sortedDict)
    
    def __patternZip(self):
    #combines select pattern data
        newDict = {}
        for i in range(1,(len(self.patterns))):
            s = [self.patterns[i],self.data.PatternFreqCnt[i]]
            newDict[self.patterns[i]] = self.data.PatternFreqCnt[i]

        for i in newDict.keys():
            if newDict[i] == None:
                newDict[i] = 0

        sortedDict = OrderedDict(sorted(newDict.items(),key=lambda t:t[0]))
        return(sortedDict)


