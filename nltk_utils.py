# this download was needed only once to make it work
#nltk.download('punkt')

import nltk;
from nltk.stem.porter import PorterStemmer
import numpy as np

stemmer = PorterStemmer()

# function for tokenising step
def tokenize(sentence):
    # use the nltk kit, nltk will tokenize the sentence i give
    return nltk.word_tokenize(sentence)


# function for stemming step
def stem(word):
    # use the variable stemmer from ntlk.stem.porter, then let the thing do the process
    # and lowercase the words
    return stemmer.stem(word.lower())


#test tokenisation and stemming
#a = "How long does shipping take?"
#print(a)
#a = tokenize(a)
#print(a)

#words = ["Organize", "organizes", "Organizing"]
#stemmed_words = [stem(w) for w in words]
#print(stemmed_words)





# function for bagg of words
# put tokenized_sentence in there to know that tokenisation must be applied first
def bag_of_words(tokenized_sentence, all_words):
    
    # how bag of words will look like
    # sentence = ["hello", "how", "are", "you"]
    # words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    # bag = [   0,      1,     0,    1,     0,      0,       0 ]

    # applying the stemming
    tokenized_sentence = [stem(w) for w in tokenized_sentence]

    # create a bag, and initialize it with zero for each word
    bag = np.zeros(len(all_words), dtype=np.float32)
    # numerate all words, give index and current word
    for idx, w in enumerate(all_words):
        # check, if this word is in the tokenized sentence, 
        if w in tokenized_sentence:
        # then it will get a 1
            bag[idx] = 1.0

    return bag

# testing the bag of words, the whole process made above
sentence = ["hello", "how", "are", "you"]
words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
bag = bag_of_words(sentence, words)
print(bag)
# when printing bag you can see the array [   0,      1,     0,    1,     0,      0,       0 ] from above