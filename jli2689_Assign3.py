#Author: Jiawei Li
#Student number: 250919248
#UWO username: jli2689
#This program is to calculate the average happiness score of four different time zones, according to the tweets from each time zone.


import happy_histogram

#setting constants for the time zone locations
MIN_LATITUDE = 24.660845
MAX_LATITUDE = 49.189787

LONGITUDE = -67.444574
EASTERN_LONG = -87.518395
CENTRAL_LONG = -101.998892
MOUNTAIN_LONG = -115.236428
PACIFIC_LONG = -125.242264

#define the lists
listOfKeywords = []
listOfSentiment = []

#assign variables
totalEastern = 0
sentimentEastern = 0
totalCentral = 0
sentimentCentral = 0
totalMountain = 0
sentimentMountain = 0
totalPacific = 0
sentimentPacific = 0

averageEastern = 0
averageCentral = 0
averageMountain = 0
averagePacific = 0


#define the functions needed to process keywords text file
#define the function that calls keywords file and determines if it exists
def keywordsMain():
    try:
        infile = open(input('Name of the text file you want to open: '), 'r', encoding = 'utf-8')
        processKeywords(infile)
    except IOError:
        quit('Error: file not found')
    finally:
        infile.close()

#define the function that process the file and store data into two lists
def processKeywords(infile):
    for line in infile:
        parts = line.strip().split(',')
        listOfKeywords.append(parts[0])
        listOfSentiment.append(int(parts[1]))
    return listOfKeywords, listOfSentiment

def calculateSen(text):
    global parts
    words = []
    value = 0
    tweetSen = 0
    text = parts[5]
    text = text.strip().lower()
    text = text.strip('~!@#$%&*():"<>?{}`;,./')
    words = text.split()
    for el in words:
        if el in listOfKeywords:
            pos = listOfKeywords.index(el)
            value = listOfSentiment[pos]
            #print(el, pos, value)
            tweetSen = tweetSen + value
    #print(tweetSen)
    return tweetSen

def calculateHS():
    global averagePacific, averageMountain, averageCentral, averageEastern
    averageEastern = sentimentEastern / totalEastern
    averageCentral = sentimentCentral / totalCentral
    averageMountain = sentimentMountain / totalMountain
    averagePacific = sentimentPacific / totalPacific
    return averageCentral, averageMountain, averagePacific, averageEastern

#codes using the functions above, and to process the tweets
keywordsMain()
try:
    infile = open(input('Name of the tweets file you want to open: '), 'r', encoding = 'utf-8')
    latitude = 0.0
    longitude = 0.0
    for line in infile:
        parts = line.strip().split(' ', 5)
        latitude=float((parts[0].strip('[,')))
        longitude=float((parts[1].strip(']')))
        #print(latitude,longitude)
        if calculateSen(parts[5]) != 0:
            if MIN_LATITUDE <= latitude <= MAX_LATITUDE:
                #print('a')
                if EASTERN_LONG <= longitude < LONGITUDE:
                    totalEastern = totalEastern + 1
                    sentimentEastern = sentimentEastern + calculateSen(parts[5])
                if CENTRAL_LONG <= longitude < EASTERN_LONG:
                    totalCentral = totalCentral + 1
                    sentimentCentral = sentimentCentral + calculateSen(parts[5])
                if MOUNTAIN_LONG <= longitude < CENTRAL_LONG:
                    totalMountain = totalMountain + 1
                    sentimentMountain = sentimentMountain + calculateSen(parts[5])
                if PACIFIC_LONG <= longitude < MOUNTAIN_LONG:
                    totalPacific = totalPacific + 1
                    sentimentPacific = sentimentPacific + calculateSen(parts[5])
except IOError:
    quit('ErrorL file not found')

infile.close()
calculateHS()

#print out the results
print('The happiness score for Eastern time zone is ' + str(averageEastern))
print('The number of tweets found in Eastern time zone is ' + str(totalEastern))

print('The happiness score for Central time zone is ' + str(averageCentral))
print('The number of tweets found in Central time zone is ' + str(totalCentral))

print('The happiness score for Mountain time zone is ' + str(averageMountain))
print('The number of tweets found in Mountain time zone is ' + str(totalMountain))

print('The happiness score for Pacific time zone is ' + str(averagePacific))
print('The number of tweets found in Pacific time zone is ' + str(totalPacific))

# draw the histogram
happy_histogram.drawSimpleHistogram(str(totalEastern), str(totalCentral), str(totalMountain), str(totalPacific))
