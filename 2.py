import happy_histogram

file_keywords = None
file_tweets = None

# score = suml of happiness scores of all keywords / number of keywords
# Ignore the tweet if it is not containing any keyword
# happiness scores of a region = sum of happiness scores of all tweets in that region / number of tweets
def Calculate_happiness_score():
        for region in list_of_region:
                total = 0
                no_of_tweets = 0

                # calculate score
                for itr in happiness_scores[region][0]:
                        tweetScore = 0
                        no_of_keywords = 0
                        for tweetWord in itr:
                                # remove all unnecessary symbols
                                word = tweetWord.strip('/^"`&@_*\'•“”~[]<>()-+=0123456789»%$:\!.?#,;')
                                word = word.lower()

                                if word in keywords:
                                        tweetScore = tweetScore + keywords[word]
                                        no_of_keywords += 1

                        if      no_of_keywords != 0:
                                total += tweetScore/no_of_keywords
                                no_of_tweets += 1
                        else:
                                total += 0

                happiness_scores[region][1] = no_of_tweets

                if no_of_tweets != 0:
                        happiness_scores[region][2] = total/no_of_tweets
                else:
                        happiness_scores[region][2] = 0


while file_keywords == None:
        try:
                filename=input("Enter the name of the keywords file here: ")
                file_keywords = open(filename, "r")
        except IOError as err:
                print(err)

while file_tweets == None:
        try:
                file_tweets = open(input("Enter the name of the tweets file here: "), "r")
        except IOError as err:
                print(err)

# {region: [tweets], num of valid tweets, num of keywords, region score, num of tweets}
happiness_scores = {'eastern': [[], 0, 0, 0], 'central': [[], 0, 0, 0], 'mountain': [[], 0, 0, 0], 'pacific': [[], 0, 0, 0]}
list_of_region = ['eastern', 'central', 'mountain', 'pacific']

keywords = {}

# extract the keywords and values from the keywords file
for line in file_keywords:
        word,value=line.split(',')
        value=int(value)
        keywords[word] = value

# Processing the tweets file
for line in file_tweets:
        lst = line.split()
        lat = lst[0].strip('[')
        lat = float(lat.rstrip(','))
        long = float(lst[1].rstrip(']'))

        # Filtering out the region that are not in valid range
        if lat > 49.189787 or lat < 24.660845:
                continue
        if long > -67.444574 or long < -125.242264:
                continue

        # Figuring out the region from where the tweet was made
        if long <= -115.236428:
                region = 'pacific'
                happiness_scores['pacific'][3] += 1
        elif long <= -101.998892:
                region = 'mountain'
                happiness_scores['mountain'][3] += 1
        elif long <= -87.518395:
                region = 'central'
                happiness_scores['central'][3] += 1
        elif long <= -67.444574:
                region = 'eastern'
                happiness_scores['eastern'][3] += 1

        # Removing unnecessary content from tweet
        line = line.replace(', ', '', 4)
        line = line.replace('.', '', 2)
        line = line.replace('.', ' ')
        line = line.replace(', ', ' ')
        lst = line.split()
        lst = lst[4:]

        # Appending the information to the list happiness_scores
        happiness_scores[region][0].append(lst)

file_keywords.close()
file_tweets.close()
Calculate_happiness_score()

for region in list_of_region:
        print("Region " + region + ":::")
        print("Total number of tweets: " +  str(happiness_scores[region][3]) + "\nNumber of valid tweets: " + str(happiness_scores[region][1]) + "\n Region happiness score: " + str(happiness_scores[region][2]) + "\n")

# draw the happy histogram
happy_histogram.drawSimpleHistogram(happiness_scores['eastern'][2], happiness_scores['central'][2], happiness_scores['mountain'][2], happiness_scores['pacific'][2])
