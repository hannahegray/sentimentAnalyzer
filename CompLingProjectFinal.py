# Comp 294-02: Final Project 
# Author: Hannah Gray 
# Date: 5/7/16



#============================
# Imports
import nltk 
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
import re


#============================
# Variables
negDict = {}
posDict = {}

reviewWords = {}

titles = ["223207", "222692", "232806", "215143", "191695", "234420", "236310","207730","222234", "231744","235408","217040", "237440", "207654", "219262", "233127", "220973", "232837", "229422", "194397"]

negCount = [] 
posCount = [] 
negWord = []
posWord = []
#=============================
# Functions 

def wordList(text): 
    """Takes the unicode text from the review and splits it up into the individual words.
    Takes out stopwords as well."""
    wordList = []
    splits = text.split()
    for word in splits:
        if word not in wordList:
            if word.lower() not in stopwords.words("german"):   #worry about numbers and punctuation later
                wordList.append(word)
    #print wordList
    return wordList
    

def cleanStar(stars):
    """Takes the unicode string of the rating and changes it into a float integer from -3 to 2"""
    star = re.sub("[^1-9,]", "", stars)    #gets rid of extra words/spaces, leaves only numbers in the string
    if star == u'0':
        newStar = -3
    elif star == "0,5":
        newStar = -2.5
    elif star == "1":
        newStar = -2 
    elif star == "1,5":
        newStar = -1.5
    elif star == "2":
        newStar = -1
    elif star == "2,5":
        newStar = -.5
    elif star == "3":
        newStar = 0
    elif star == "3,5":
        newStar = .5
    elif star == '4':
        newStar = 1
    elif star == '4,5':
        newStar = 1.5
    elif star == '5':
        newStar = 2
    #print newStar
    return newStar


def findWords(movies):
    """finds the reviews and star ratings for each movie, cleans up the text and changes the rating from a star into 
    a integer from -3 to 2. This value is assigned to each of the words in the text of each review."""
    for movie in movies:
        fileIn = open(movie+ ".html", 'r') 
        words = fileIn.read()
        soup = BeautifulSoup(words, "html.parser")
        rating = soup.find_all("div", itemprop="review")                       #finds every individual review of the movie
    
        for i in rating:
            text = i.find(itemprop = 'description').text
            cleanT = wordList(text)                                            #find the text in that review
            star = i.find(class_="vam lighten", itemprop = 'ratingValue').text #find the numerial star rating for the review
            cleanS = cleanStar(star)
            
            for word in range(len(cleanT)):
                if cleanT[word] not in reviewWords:                            #looks to see if the word is in the dictionary of review
                    reviewWords[cleanT[word]] = [cleanS]              #adds the word if it is not in dict, the value is the star rating 
                else:
                    reviewWords[cleanT[word]].append(cleanS)          #adds another star rating if word is already in dict
    #print reviewWords
    return reviewWords


def sort(dictionary):
    """Sorts the words from reviewWords dictionary into positive or negative sentiments based on the average rating they
    are used in"""
    for i in dictionary.keys():                                 #gets the name of the key 
        value = dictionary.get(i)                               #gets value     
        average = sum(value)/len(value)    #finds the average star rating of word (based on ratings of reviews that word is found in
        if average >= 0:
            posDict[i] = average            #decides where word has an overall "positive" or overall "negative" sentiment
        else:
            negDict[i] = average 
    #print posDict                          #unhash to see what the dictionary is 
    #print negDict                          #unhash to see what the dictionary is

    
def dataCollection():
    """Takes nothing as an input, creates the positive and negative dictionaries from the web pages at filmstarts.de. Calls all of the functions defined above."""
    words = findWords(titles)
    dicts = sort(words)
    return dicts
    

def cleanInput(words):
    """takes a string as input and returns the unicode version of it, split into individula words on whitespace"""
    wordsU = unicode(words, "utf-8")
    splits = wordsU.split()
    return splits 
    
def average(counts):
    """averages the positiity or negativity scores of a sentence"""
    if len(counts) == 0:
        total = 0
    else:
        total = sum(counts)/len(counts) 
    return total
    
def organize(text):
    """goes through the input sentence and tallies the "positive" words in the sentence as well as the "negative" words. 
    Then averages the total scores and find total "positivness" and "negativeness" of words."""
    negCount = [] 
    posCount = [] 
    negWord = []
    posWord = []    
    for word in text:
        if word in posDict:
            posCount.append(posDict[word])      #appends positive numerical value to the list for positive counts
            posWord.append(word)                #appends positive word to separate list for comparison's sake. 
        elif word in negDict:
            negCount.append(negDict[word])      #appends negative numerical value to negative counts list
            negWord.append(word)                #appends negative word for comparison 
    negAvg = average(negCount) 
    posAvg = average(posCount)
    
    print "-------------------------"           #prints statements to summarize what has been calculated
    print "Sentence:", text
    print "Negativity:", negAvg, negWord
    print "Positivity:", posAvg, posWord
    if posAvg > abs(negAvg):                                 #makes sentence positive if positve average is greater than negative
        print "This is an overall positive sentence"    
        print "----------------------------"
    elif abs(negAvg) > posAvg:                               #makes sentence negative if negative average is greater than positive
        print "THis is an overall negative sentence"
        print "----------------------------"
    elif abs(negAvg) == posAvg:                              # makes sentnce neutral if the averages are equal
        print "This sentence is neither positive nor negative"
        print "----------------------------"


def dataAnalysis(string):
    """takes strings of sentences as input and analyzes them based on the film sentiment dictionary"""
    dataCollection()
    cleanI = cleanInput(string)
    organize(cleanI)
    
#===============================
# Script
example = "der Film ist süß"    
    #The film is sweet 
example1 = "ich hasse der Film. Er war sehr langweilig"     
    #I hate the Film. It was very boring
example2 = "die Animationen waren sehr schön aber ich habe keine Ahnung worum geht der Film."    
    #The animation was very beautiful but I don't have any idea what the film was about. 
example3 = "mehr Animationen wären schlecht " 
    #more animations would be bad.
example4 = "mehr Animationen wären gut"
    #more animations would be good. 

#dataAnalysis(example)
#dataAnalysis(example1) 
#dataAnalysis(example2)
#dataAnalysis(example3)
#dataAnalysis(example4)

#================================
# Final Thoughts 
"""This project did not work as well as I thought it was going to. I think I need to get a lot more 
data in order for the dictionary to be comprehensive enough to get a good idea of scores. Also word
sentiment changes depending on the context and other words around it, which this code does not really 
take into consideration. I would like to try using bigrams to analyze the sentiments but I would need 
more data because I don't have enough data to get really get a good sense of important bigrams in the 
reviews. 

When you look at the 5 example sentences I ran through my program, you can tell that it works well for 
the simple sentences, but there are not enough words in my dictionary to give an accurate representation 
for all sentenes. In example, my code gets the right answer because "Film" and "süß" are in the dictionary
However, in example1, the program gets it wrong because neighter the word "hasse" or "langweilig" appear
in the dictionary, and those are the words that carry the most sentiment and meaning in that sentence. 

The same thing happens in example2 because the programs has enough words to analyze the first part of the 
sentence (the more positive part), but not the second part (which is less positive). 

The last two texts, example3 and example4 are both right! The program correctly weights and calculates how 
positive or negative the sentence is. Eventually I want to get it to work like that for all of my sentences. 

Overall I'm happy with what I was able to accomplish, but it could be a fun project to work on furhter in 
the future."""
