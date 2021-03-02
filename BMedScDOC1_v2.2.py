#BMedSc DOC v2 script
#The aim of this script is to transpose a pdf study into a txt 
#Then run a search for specific terms from a dictionary within the txt file
#Then output a bar graph of all dictionary terms

#Usage: python BMedScDOC1_v1.py [dictionary.txt] [study.txt]

import sys
import re
from collections import Counter
import pdfplumber
import matplotlib
import matplotlib.pyplot as plt
import numpy

dictionary = []
text = []
relevant = []

#main function
def main():
    if len(sys.argv) != 3: #This needs to be changed to 3 soon
        print('Usage: python BMedScDOC1_v1.py [dictionary.txt] [study.pdf]')
        sys.exit(1)
    dictionary = makedict(sys.argv[1])
    print(dictionary)
    text = maketxt(pdftotxt(sys.argv[2]))
    print(text)
    relevant = search(dictionary, text)
    finalwords = Counter(relevant).most_common()
    print(finalwords)
    plotwords(finalwords)
    

    
#Make dictionary list from txt file
def makedict(textfile):
    with open(textfile, 'r') as file:
        dictionary = file.read().replace('\n', ' ')
        dictionary = dictionary.lower().split()
        return dictionary
    

#Convert a pdf to a txt file
def pdftotxt(text):
    with pdfplumber.open(text) as pdf:
        with open("{}.txt".format((sys.argv[2])[:-4]), "a") as output:
            for i in range(len(pdf.pages)):
                page = pdf.pages[i]
                output.write(page.extract_text())
    return "{}.txt".format((sys.argv[2])[:-4])
    
    
#Create list of words appearing in txt file
def maketxt(text):
    string = ''
    with open(text) as file:
        string = file.read()
        string = re.sub('[^\w\s]', '', string) #only whitespace + alphanum chars. Use regex to refine this more
        string = re.sub("\d+", '', string) #remove numeric chars. Use regex to refine this more
        string = string.lower().split()
        return string
        
    
#Collect all dictionary terms into one list with repeats
def search(dictionary, text):
    relevant = []
    for word in text:
        if word in dictionary:
            relevant.append(word)
    return relevant


#plot words in a bar graph
def plotwords(list_of_tuples):
    plotdata = ([ a for a,b in list_of_tuples ], [ b for a,b in list_of_tuples ])
    
    #split x and y axis values into separate lists
    words = plotdata[0]
    occurrences = plotdata[1]
    
    #use pyplot the graph
    plt.figure(figsize=(9, 3))
    plt.plot()
    plt.bar(words, occurrences)
    
    #title and labels for graph
    plt.title("BMedScDOC words in text from {}".format(sys.argv[1]))
    plt.ylabel("Number of occurrences")
    plt.xlabel("Words from dictionary")
    #all done!
    plt.show()
    


main()
sys.exit(0)