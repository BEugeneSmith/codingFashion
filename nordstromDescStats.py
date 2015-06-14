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
                'Houndstooth','Contrast','Print','Lace',
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

class colorDataPrep:
    def __init__(self,df):
        self.df = df
        self.freqTable = self.__colorFreqTable()
        self.totalColors = sum(self.freqTable.values())
        self.ratioTable = self.__percentageTable()
        
    def __colorFreqTable(self):
    #creates a table of frequency for all of the item names
        colors = self.df['binnedColor'].tolist()
        
        freqTable = {}
        for color in colors:
            freqTable[color] = freqTable.get(color,0)+1
     
        return(freqTable)
    
    def __percentageTable(self):
        ratio = self.freqTable
        
        for color in ratio.keys():
            perc = 100 * (ratio[color]/float(self.totalColors))
            ratio[color] = perc
        return(ratio)

class itemReduce(Props):
    
    def __init__(self,df):
        Props.__init__(self)
        self.df = df
        self.df['item'] = self.__extractedPieces()
        self.df['pattern'] = self.__extractedPatterns()
        self.df['texture'] = self.__extractedTextures()
        self.df['fit'] = self.__extractedFits()
    
    #apply these two methods to the other three parameters
    def __translatePiece(self,item):
        for piece in self.items:
            testPiece = re.findall(piece,item)
            if testPiece:
                return testPiece
            elif not testPiece and piece == self.items[-1]:
                return ['unsorted']
            else:
                next
            
    def __extractedPieces(self):
        array = []
        for item in self.df['ItemName']:
            array.append(self.__translatePiece(item))
        return(sum(array,[]))
  

    def __translatePattern(self,item):
        for pattern in self.patterns:
            testPattern = re.findall(pattern,item)
            if testPattern:
                return testPattern
            elif not testPattern and pattern == self.patterns[-1]:
                return ['unsorted']
            else:
                next
            
    def __extractedPatterns(self):
        array = []
        for item in self.df['ItemName']:
            array.append(self.__translatePattern(item))
        combinedArray = sum(array,[])
        del combinedArray[-1] 
        return(combinedArray)
    
    
    def __translateTexture(self,item):
        for texture in self.textures:
            testTexture = re.findall(texture,item)
            if testTexture:
                return testTexture
            elif not testTexture and texture == self.textures[-1]:
                return ['unsorted']
            else:
                next
          
    def __extractedTextures(self):
        array = []
        for item in self.df['ItemName']:
            array.append(self.__translateTexture(item))
        combinedArray = sum(array,[])
        del combinedArray[-1] 
        del combinedArray[-2]
        del combinedArray[-3] 
        return(combinedArray)
    
    def __translateFit(self,item):
        for fit in self.fits:
            testFit = re.findall(fit,item)
            if testFit:
                return testFit
            elif not testFit and fit == self.fits[-1]:
                return ['unsorted']
            else:
                next
          
    def __extractedFits(self):
        array = []
        for item in self.df['ItemName']:
            array.append(self.__translateFit(item))
        combinedArray = sum(array,[])
        return(combinedArray)
    
class colorReduce:
    #returns pandas dataframe with reduced colors
    
    def __init__(self,pdDF):
        self.pdDF = pdDF
        self.nordstromColors = self.pdDF['Color']
        self.colorTdDict = self.__colorTDict()
        self.basicColors = self.colorTdDict.keys()
        self.reducedColors = self.__colorListTranslate()
        self.__newDF()
    
    def __colorTDict(self): 
        return {
            #Reds
            'Red':'Red',
            'Claret':'Red',
            'Pink':'Red',
            'Burgundy':'Red',
            'Wine':'Red',
            'Cherry':'Red',
            'Fuchsia':'Red',
            'Orchid':'Red',
            'Strawberry':'Red',
            'Rose':'Red',
            'Raspberry':'Red',
            'Coral':'Red',
            'Grenadine':'Red',
            'Pinot':'Red',
            'Bordeaux':'Red',
            'Berry':'Red',
            'Salmon':'Red',
            'Ginger':'Red',
            'Auburn':'Red',
            'Cranberry':'Red',
            'Flamingo':'Red',
            'Petal':'Red',
            'Crimson':'Red',
            'Beet':'Red',
            'Blush':'Red',
            'Cayenne':'Red',
            'Garnet':'Red',
            'Geranium':'Red',
            'Pepper':'Red',
            'Bricks':'Red',
            'Magenta':'Red',
            'Rosa':'Red',
            'Fuschia':'Red',
            'Rouge':'Red',
    
            #Oranges
            'Orange':'Orange',
            'Tangerine':'Orange', 
            'Nectarine':'Orange', 
            'Sunrise':'Orange', 
            'Horizon':'Orange',
            'Cinnamon':'Orange',
            'Rust':'Orange',
            'Apricot':'Orange',
            'Yam':'Orange',
            'Clementine':'Orange',
            'Spice':'Orange',
            'Melon':'Orange',
            'Dusk':'Orange',
            'Peach':'Orange',
            'Marigold':'Orange',
            'Guava':'Orange',
            'Hibiscus':'Orange',
            'Mango':'Orange',
            'Papaya':'Orange',
            'Saffron':'Orange',
            'Guava':'Orange',
            'Amber':'Orange',
            'Ambrosia':'Orange',
            'Canteloupe':'Orange',
            'Persimmon':'Orange',
            
            #Yellows
            'Yellow':'Yellow',
            'Gold':'Yellow',
            'Cumin':'Yellow',
            'Lemon':'Yellow',
            'Citrus':'Yellow',
            'Honey':'Yellow',
            'Champagne':'Yellow',
            'Citrine':'Yellow',
            'Pineapple':'Yellow',
            'Wheat':'Yellow',
            'Lemondrop':'Yellow',
            'Sundrop':'Yellow',
            
            #Greens
            'Green':'Green',
            'Moss':'Green',
            'Olive':'Green',
            'Army':'Green',
            'Lime':'Green',
            'Kelp':'Green',
            'Mint':'Green',
            'Seafoam':'Green',
            'Sea':'Green',
            'Sage':'Green',
            'Grass':'Green',
            'Leaf':'Green',
            'Verdugo':'Green',
            'Celery':'Green',
            'Cilantro':'Green',
            'Camo':'Green',
            'Palm':'Green',
            'Thistle':'Green',
            'Thyme':'Green',
            'Spearmint':'Green',
            'Aloe':'Green',
            'Cactus':'Green',
            'Cypress':'Green',
            'Eucalyptus':'Green',
            'Jade':'Green',
            'Kale':'Green',
            'Kiwi':'Green',
            'Peridot':'Green',
            'Vermillion':'Green',
            'Vernet':'Green',
            'Malachite':'Green',
            'Pear':'Green',
    
            #Blues
            'Blue':'Blue',
            'Marine':'Blue',
            'Teal':'Blue',
            'Turquoise':'Blue',
            'Navy':'Blue', 
            'Denim':'Blue',
            'Atlantic':'Blue',
            'Aqua':'Blue',
            'Indigo':'Blue',
            'Sky':'Blue',
            'Midnight':'Blue',
            'Sapphire':'Blue',
            'Royal':'Blue',
            'Ocean':'Blue',
            'Lake':'Blue',
            'Maritime':'Blue',
            'Wave':'Blue',
            'Blueberry':'Blue', 
            'Neptune':'Blue',
            'Cobalt':'Blue',
            'Cyan':'Blue',
            'Azure':'Blue',
            'Wash':'Blue',
            'Wave':'Blue',
            'Night':'Blue',
            'Atlantis':'Blue',
            'Water':'Blue',
            'Lagoon':'Blue',
            'Coneflower':'Blue',
            'Cerulean':'Blue',
            'Chartreuse':'Blue',
            'Chartruse':'Blue',
            'Cornflower':'Blue',
            'Marina':'Blue',
    
            #Purples
            'Purple':'Purple',
            'Lilac':'Purple',
            'Violet':'Purple',
            'Lavender':'Purple', 
            'Periwinkle':'Purple',
            'Grape':'Purple',
            'Amethyst':'Purple',
            'Mulberry':'Purple',
            'Plum':'Purple',
            'Pomegranate':'Purple',
            'Raisin':'Purple',
            'Viola':'Purple',
            
            #Blacks
            'Black':'Black',
            'Charcoal':'Black',
            'Ink':'Black',
            'Shadow':'Black',
            'Caviar':'Black',
            'Coal':'Black',
            'Noir':'Black',
    
            #Grays
            'Gray':'Grey', 
            'Silver':'Grey',
            'Graphite':'Grey', 
            'Grey':'Grey',
            'Asphalt':'Grey',
            'Ash':'Grey',
            'Stone':'Grey', 
            'Pavement':'Grey',
            'Platinum':'Grey',
            'Granite':'Grey',
            'Slate':'Grey',
            'Smoke':'Grey',
            'Gravel':'Grey',
            'Metal':'Grey',
            'Tin':'Grey',
            'Pewter':'Grey',
            'Pebble':'Grey',
            'Alloy':'Grey',
            'Concrete':'Grey',
            'Elephant':'Grey',
            'Cement':'Grey',
            'Flint':'Grey',
            'Gunmetal':'Grey',
            
            #Whites
            'White':'White',
            'Cream':'White',
            'Creme':'White',
            'Ivory':'White',
            'Bone':'White',
            'Rice':'White',
            'Arroyo':'White',
            'Eggshell':'White',
            'Chalk':'White',
            'Pearl':'White',
            'Linen':'White',
            'Porcelain':'White',
            'Powder':'White',
            'Vanilla':'White',
            'Whey':'White',
            'Alabaster':'White',
            'Pumice':'White',
            
            #Browns
            'Brown':'Brown',
            'Coffee':'Brown',
            'Khaki':'Brown', 
            'Tan':'Brown',
            'Beige':'Brown',
            'Camel':'Brown',
            'Natural':'Brown',
            'Oatmeal':'Brown',
            'Chocolate':'Brown', 
            'Cappuccino':'Brown', 
            'Caramel':'Brown',
            'Mushroom':'Brown',
            'Desert':'Brown',
            'Dune':'Brown',
            'Sand':'Brown',
            'Tobacco':'Brown',
            'Taupe':'Brown',
            'Peanut':'Brown',
            'Rope':'Brown',
            'Straw':'Brown',
            'Butterscotch':'Brown',
            'Scotch':'Brown',
            'Whiskey':'Brown',
            'Beeswax':'Brown',
            'Peat':'Brown',
            'Cognac':'Brown',
            'Cocoa':'Brown',
            'Espresso':'Brown',
            'Java':'Brown',
            'Mauve':'Brown',
            'Buff':'Brown',
            'Tea':'Brown',
            'Tiramisu':'Brown',
            'Mocha':'Brown',
            }
    
    def __colorTranslate(self,nColor):
        for color in self.basicColors:
            testColor = re.findall(color,nColor)
            if testColor:
                return self.colorTdDict[testColor[0]]
            elif not testColor and color == self.basicColors[-1]:
                return 'unsorted'

    def __colorListTranslate(self):
        reducedColors = []
        for color in self.nordstromColors:
            reducedColors.append(self.__colorTranslate(color))
        return(reducedColors)
        
    def __newDF(self):
        self.pdDF['binnedColor'] = self.reducedColors
