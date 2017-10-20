import webbrowser, requests, bs4, re, math, statistics
#Green PC Computer Price Estimator
#by DeMarco Best II
#This program seeks to scrape ebay for part prices and use them to estimate average pc parts
#Program attempts to remove outlier prices from ebay by taking an intial average, calculating the standard deviation based on that average, then removes data points that are more than 1.5 standard deviation away from the mean. 
#The new part mean will be calculated using the remaining data

print('Welcome to the Computer Price Calculator')

def computerDictionaryBuilder():
    #Sets up Generic RAM speed to be used later, and the dictionary for PC Attributes
    pcAttributesDictionary  = {}
    urlList = []
    defaultsearchString = 'https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw='
    defaultURLEnding = '&_dcat=27386&rt=nc&LH_ItemCondition=3000_ipg=2000000000&LH_FS&LH_BIN=1'
    searchString = ''
    genericRAMSpeedDDR4 = '2133'
    genericRAMSpeedDDR3 = '1333'

    #Asks if the PC in question is a laptop and creates appropriate dictionary entry in response
    laptopDesktopQuery = input('Is it a laptop or desktop? ')
    if laptopDesktopQuery.lower() == 'laptop':
         pcAttributesDictionary['Laptop?'] = True
    elif laptopDesktopQuery.lower() == 'desktop':
         pcAttributesDictionary['Laptop?'] = False
    
    #In the case that it isn't a laptop, asks if its a custom or refurb and creates appropriate dictionary entry
    if  pcAttributesDictionary['Laptop?'] == False:
        refurbCustomQuery = input('Is it a custom or refurb?')
        if refurbCustomQuery.lower() == 'custom':
             pcAttributesDictionary['Custom?'] = True
        elif refurbCustomQuery == 'refurb':
             pcAttributesDictionary['Custom?'] = False

    #In the case that it is a laptop, asks for the laptop's model number
    elif  pcAttributesDictionary['Laptop'] == True:
         pcAttributesDictionary['Model Number'] = input("What model laptop is it?")
         searchString = defaultsearchString + pcAttributesDictionary['Model Number'] + defaultURLEnding
         urlList.append(searchString)
    
    #In the case that it is a custom PC, asks for the PC's Specs
    if  pcAttributesDictionary['Custom?'] == True:
        print('I\'m going to collect some hardware data now.')
        pcAttributesDictionary['CPU'] = input('What CPU is it?')
        pcAttributesDictionary['RAM Type']= input('What type of RAM does it have? EX(DDR3, DDR4)')
        pcAttributesDictionary['RAM Capacity']= input('How much RAM does it have?')
        pcAttributesDictionary['GPU']= input('What GPU does the computer have?')
        pcAttributesDictionary['Has SSD?'] = input('Does it have an SSD? Enter \'Yes\' or \'No\'')
        if  pcAttributesDictionary['Has SSD?'].lower() == 'yes':
            pcAttributesDictionary['SSD Capacity'] = input('What capacity is the SSD? ')
            searchString = defaultsearchString + pcAttributesDictionary['SSD Capacity'] + '%20' + 'SSD' + defaultURLEnding
            urlList.append(searchString)

        elif pcAttributesDictionary['Has SSD?'].lower() == 'no':
            pcAttributesDictionary['Has HDD'] = 'Yes'
            pcAttributesDictionary['HDD Capacity'] = input('What is the capacity of the HDD? ')
            searchString = defaultsearchString + pcAttributesDictionary['HDD Capacity'] + defaultURLEnding
            urlList.append(searchString)
        
        searchString = defaultsearchString + pcAttributesDictionary['CPU'] + defaultURLEnding
        urlList.append(searchString)
        searchString = defaultsearchString + pcAttributesDictionary['RAM Type'] + '%20' + pcAttributesDictionary['RAM Capacity'] + defaultURLEnding
        urlList.append(searchString)
        searchString = defaultsearchString + pcAttributesDictionary['GPU'] + defaultURLEnding
        urlList.append(searchString)

    elif pcAttributesDictionary['Custom?'] == False:
        pcAttributesDictionary['Computer Model Number'] = input('What is the model of the Computer?')
        searchString = defaultsearchString + pcAttributesDictionary['Computer Model Number'] +defaultURLEnding
        urList.append(searchString)
    


    return urlList

#Creating the global dictionary that we'll be using.       


#Legacy Search Query for finding out the product search. To be phased out.
#searchQuery = input('What are we searching for? ')

#Legacy Condition Query for finding out the condition code, to be phased out.
#conditionQuery = input('What item condition are we looking for? ')

#Disects the input string using whitespace seperators, while slipping it into a list
#searchList = searchQuery.split()

#Sets the condition code for later use in URL building
#if conditionQuery.lower() == 'used':
    #conditionCode = '3000'

#elif conditionQuery.lower() == 'new':
    conditionCode = '1000'
#else:
    #print('Error')

def buildURL(searchString):
    #The required prefix for every ebay search URL
    searchURL = 'https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw='
    #Iterates through searchString and builds up a search URL
    for x in range(0,len(searchString)):
        if x == 0:
            searchURL = searchURL + searchString[x]
        else:
            searchURL = searchURL + '%20' + searchString[x]
    #Adds the suffix for URL, includes item condition, results desired, buy it now setting and free shipping (maybe)
    searchURL = searchURL + '&_dcat=27386&rt=nc&LH_ItemCondition=' + conditionCode + '_ipg=2000000000&LH_FS&LH_BIN=1'
    return searchURL

def iterativeScrape(urlList):
    additiveList = []
    for x in range(0,len(urlList)):
        # This part here combs the site and pulls down the HTML code
        ebayResultsR = requests.get(urlList)
        ebayResultsBS = bs4.BeautifulSoup(ebayResultsR.text)

        #Setting up a regular expression that looks for dollar values of any size
        priceRexMoney = re.compile(r'\$\d*\.\d{2}(?!\sshipping)')

        #Magics the Soup into a String, then searches it for dollar values
        priceList = priceRexMoney.findall(str(ebayResultsBS))

        #Combines priceList into a single string
        for x in range(0,len(priceList)):
            if x == 0:
                priceString = priceList[x] + priceList[x+1]
            else:
                priceString = priceString + priceList[x]

        #Seperates that string to get rid of the dollar signs
        newPriceList = priceString.split('$')

        #Deletes this odd empty spot in the first index of the list that appears for no reason
        del newPriceList[0]
        lenofList = len(newpriceList)
        discardedPrices = []
        accumulator1 = 0
        #Polymorphs the strings in the priceList into floats so we can do math with them.
        for x in range(0,lenofList):
            newpriceList[x] = float(newpriceList[x])

        
        #Calculates the mean of the scraped data
        floatAverage = statistics.mean(newpriceList)
        #Calculates standard deviation of scraped data
        standardDev = statistics.pstdev(newpriceList)
        
        
        #If any value in the list is greater than 1.5 SD's away from the mean, discard it
        for x in range (0,lenofList):
            standardScore = (newpriceList[x] - floatAverage)/standardDev

            if standardScore > .75 or standardScore < -.75:
                discardedPrices.append(newpriceList[x])
            
            else:
                continue
        
        #Copies the list for manipulation
        purgedData = newpriceList
        
        #Set Sample Size variable for later use
        sampleSize = 0
        theEndPriceList = []
        
        #If the data matches any of the discarded prices, its set to zero. This is the solution I came up with after realizing that for loop ranges aren't dynamic, so removing indicies from the list screws it up
        for x in range(0,len(purgedData)):
            if purgedData[x] in discardedPrices:
                purgedData[x] = 0
            else:
                continue
        #This adds one to the sample size for every piece of data that's greater than zero. This should filter out all of my "non enteries" so that my average isn't messed up in the end
        for x in range(0,len(purgedData)):
            if purgedData[x] > 0:
                sampleSize += 1
                theEndPriceList.append(purgedData[x])
            else:
                continue

        #Resets the accumulator variable which I'm sure I've used before
        accumulator = 0

        #Accumulating for the average calculation    
        for x in range(0,len(purgedData)):
            accumulator += purgedData[x]    
        #Doing the actual average
        newAverage = accumulator/sampleSize
        newstandardDev = statistics.pstdev(theEndPriceList)

        additiveList.append(newAverage)
    print(additiveList)
    
    
    

def scrape(URL):
    # This part here combs the site and pulls down the HTML code
    ebayResultsR = requests.get(URL)
    ebayResultsBS = bs4.BeautifulSoup(ebayResultsR.text)

    #Setting up a regular expression that looks for dollar values of any size
    priceRexMoney = re.compile(r'\$\d*\.\d{2}(?!\sshipping)')

    #Magics the Soup into a String, then searches it for dollar values
    priceList = priceRexMoney.findall(str(ebayResultsBS))

    #Combines priceList into a single string
    for x in range(0,len(priceList)):
        if x == 0:
            priceString = priceList[x] + priceList[x+1]
        else:
            priceString = priceString + priceList[x]

    #Seperates that string to get rid of the dollar signs
    newPriceList = priceString.split('$')

    #Deletes this odd empty spot in the first index of the list that appears for no reason
    del newPriceList[0]
    return newPriceList
    
def doingtheMath(newpriceList):
    lenofList = len(newpriceList)
    discardedPrices = []
    accumulator1 = 0
    #Polymorphs the strings in the priceList into floats so we can do math with them.
    for x in range(0,lenofList):
        newpriceList[x] = float(newpriceList[x])

    
    #Calculates the mean of the scraped data
    floatAverage = statistics.mean(newpriceList)
    #Calculates standard deviation of scraped data
    standardDev = statistics.pstdev(newpriceList)
    
    
    #If any value in the list is greater than 1.5 SD's away from the mean, discard it
    for x in range (0,lenofList):
        standardScore = (newpriceList[x] - floatAverage)/standardDev

        if standardScore > .75 or standardScore < -.75:
            discardedPrices.append(newpriceList[x])
        
        else:
            continue
    
    #Copies the list for manipulation
    purgedData = newpriceList
    
    #Set Sample Size variable for later use
    sampleSize = 0
    theEndPriceList = []
    
    #If the data matches any of the discarded prices, its set to zero. This is the solution I came up with after realizing that for loop ranges aren't dynamic, so removing indicies from the list screws it up
    for x in range(0,len(purgedData)):
        if purgedData[x] in discardedPrices:
            purgedData[x] = 0
        else:
            continue
    #This adds one to the sample size for every piece of data that's greater than zero. This should filter out all of my "non enteries" so that my average isn't messed up in the end
    for x in range(0,len(purgedData)):
        if purgedData[x] > 0:
            sampleSize += 1
            theEndPriceList.append(purgedData[x])
        else:
            continue

    #Resets the accumulator variable which I'm sure I've used before
    accumulator = 0

    #Accumulating for the average calculation    
    for x in range(0,len(purgedData)):
        accumulator += purgedData[x]    
    #Doing the actual average
    newAverage = accumulator/sampleSize
    newstandardDev = statistics.pstdev(theEndPriceList)
    
        
    #Dictionary for holding data.
    statisticsDicti = {'Average Price':floatAverage,'Standard Deviation':standardDev, 'New End Average': newAverage, 'New Standard Deviation': newstandardDev}

    #Sorts the data from lowest to highest.
    theEndPriceList = sorted(theEndPriceList)

    #Makes Entries for the min and max of the data
    statisticsDicti['New Minimum'] = theEndPriceList[0]
    statisticsDicti['New Maximum'] = theEndPriceList[len(theEndPriceList)-1]

    #Stores the price list in the dictionary
    statisticsDicti['New Price List'] = theEndPriceList

    return statisticsDicti


    
#doingtheMath(scrape(buildURL(searchList)))
iterativeScrape(computerDictionaryBuilder())

uselessThing = input('Press enter to end.')    

