import urllib
import re
import sqlite3

class Pages:

    def __init__(self,department):
        self.department = department
        self.URL = self.startingURL()
        self.ProductsHTML = self.collectCompressHTML(self.URL)
        self.MaxPages = self.extractMaxPageNumber()
        self.pageURLs = self.pageURLext()
        self.itemAA = []
        self.extractItems()

    def startingURL(self):
        #selects starting URL based on whether we are getting resources for Men or Women
        if self.department == "W":
            return("http://shop.nordstrom.com/c/all-womens-clothing?origin=leftnav")
        else:
            return("http://shop.nordstrom.com/c/all-mens-sale?origin=leftnav")

    def collectCompressHTML(self,URL):
        #retrieves HTML then strips it of tabs, new line, and carriage characters
        response = urllib.urlopen(URL)
        text = response.read()
        compressedHTML = re.sub(r"[\t\n\r]","",text.strip())
        return(compressedHTML)

    def extractMaxPageNumber(self):
        #extracts the maximum number of pages for the clothing department
        pageNums = re.findall('<ul class="product-results-pagination truncated-pagination">.*</nav>',self.ProductsHTML)
        pageNList = re.findall('data-page="(\d{1,3})"',pageNums[0])
        for i in range(0,len(pageNList)):
            pageNList[i] = int(pageNList[i])
        return(max(pageNList))

    def pageURLext(self):
        #creates list of page urls
        pageURLs = []
        for num in range(1,(self.MaxPages+1)):
            if self.department == "W":
                URL = 'http://shop.nordstrom.com/c/all-womens-clothing?page=' + str(num)
            else:
                URL = 'http://shop.nordstrom.com/c/sale-mens-clothing?page=' + str(num)
            pageURLs.append(URL)

        return(pageURLs)

    def extractItems(self):
        #gets unique url parts for each item from a page
        for page in range(60): #this can be dynamic, for now we only take the first 30 pages
            pageHTML = self.collectCompressHTML(self.pageURLs[page])
            extractedResults = re.findall('<!-- Begin FashionResults -->(.*)<!-- End FashionResults -->',pageHTML)[0]
            extractedURLs    = re.findall('href="(/s/[-a-z]*/\d{6,8}.origin=category)"',extractedResults)
            URLs = self.itemURLCreate(extractedURLs)
            self.itemAA.append(URLs)


    def itemURLCreate(self,itemExtensions):
        #creates full urls for each item
        newURLs = []
        for i in itemExtensions:
            URL = 'http://shop.nordstrom.com' + i
            newURLs.append(URL)

        return(newURLs)


class itemMD:

    def __init__(self,URL,department):
        self.URL = URL
        self.department = department
        self.HTML = self.collectCompressHTML()
        self.vendorName = self.vendorExtract()
        self.itemName = self.nameExtract()
        self.itemID = self.itemNumberExtract()
        self.itemPrice = self.priceExtract()
        self.itemColor = self.colorExtracter()

    def collectCompressHTML(self):
        #see above
        response = urllib.urlopen(self.URL)
        text = response.read()
        HTML = re.sub(r"[\t\n\r]","",text.strip())

        return(HTML)


    def vendorExtract(self):
        #extracts vendor name from item page
        vendorName = re.findall('<section id="brand-title".+><h2><a.+>(.*)</a></h2></section>',self.HTML)
        vendorName = replaceChars(vendorName[0])

        return(vendorName)


    def nameExtract(self):
        #extracts names from item page
        itemName = re.findall('<h1 itemprop="name">(.*)</h1></section',self.HTML)
        itemName = replaceChars(itemName[0])

        return(itemName)


    def priceExtract(self):
        #extract regular price from item page
        itemPrice = re.findall('regularPrice":"\$([\d,]{1,5}\.\d{2})"',self.HTML)
        try:
            return(itemPrice[0])
        except:
            return(0)


    def itemNumberExtract(self):
        #extracts item number from item page
        itemID = re.findall('<div class="item-number-wrapper">Item #(\d+)</div>',self.HTML)
        if not itemID:
            itemID = ['']
        return(itemID)


    def colorExtracter(self):
        #extracts color from item page
        colorElement = re.findall('<option (selected="\w{0,20}" )?value="color-\d{6,8}">([\w ]+)</option>',self.HTML)
        colorElement = re.findall('value="color-\d{6,8}">([\w ]+)</option>',self.HTML)
        colorList = []
        for color in colorElement:
            if ( color in colorList ):
                next
            else:
                colorList.append(color)

        if not colorList:
            colorList = ['']
        return(colorList)

    def export(self):
        #exports item properties as a string
        return([self.itemName,self.vendorName,self.itemID,self.itemPrice,self.itemColor])

    def dbExecute(self):
        #executes sql to build database
        conn = sqlite3.connect('nordstrom.db')
        c = conn.cursor()

        for color in self.itemColor:
            record = [self.itemName,self.vendorName,color,self.itemPrice]
            print(record)
            if self.department == "W":
                c.execute("INSERT INTO nordstromW VALUES (?,?,?,?)",record)
            else:
                c.execute("INSERT INTO nordstromM VALUES (?,?,?,?)",record)

        conn.commit()
        conn.close()
