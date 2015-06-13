import re

class colorReduce:
    #returns pandas dataframe with reduced colors
    
    def __init__(self,pdDF):
        self.pdDF = pdDF
        self.nordstromColors = self.pdDF['Color']
        self.colorTdDict = self.__colorTDict()
        self.basicColors = self.colorTdDict.keys()
        self.reducedColors = self.__colorListTranslate()
    
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
                return ''

    def __colorListTranslate(self):
        reducedColors = []
        for color in self.nordstromColors:
            reducedColors.append(self.__colorTranslate(color))
        return(reducedColors)
        
