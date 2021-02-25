#BMedSc DOC v1 script
#The aim of this script is to transpose a pdf study into a string
#Then run a search for specific terms from a dictionary

#Usage: python BMedScDOC1_v1.py [dictionary.txt] [study.txt]

import sys
import re
from collections import Counter
import pdfplumber

dictionary = []
text = []
relevant = []

#main function
def main():
    if len(sys.argv) != 3: #This needs to be changed to 3 soon
        print('Usage: python BMedScDOC1_v1.py [dictionary.txt] [study.txt]')
        sys.exit(1)
    dictionary = makedict(sys.argv[1])
    text = maketxt(sys.argv[2])
    relevant = search(dictionary, text)
    print(Counter(relevant).most_common())
    

    
#Make dictionary list from txt file
def makedict(textfile):
    with open(textfile, 'r') as file:
        dictionary = file.read().replace('\n', ' ')
        dictionary = dictionary.lower().split()
        return dictionary
        

#Make .txt file from pdf study TODO


#Create list of words appearing in txt study
def maketxt(text):
    string = ''
    with pdfplumber.open(text) as pdf:
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            string = string + page.extract_text()
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


main()
sys.exit(0)