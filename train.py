from calendar import LocaleTextCalendar
import json
from operator import le
# access the functions from the other made python file
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np
# from pytorch
import torch 
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from model import NeuralNet

# open json file and read it
with open('intents5.json', "r") as f:
    intents = json.load(f)

###print(intents)



# after reading the file, I need to collect all of the words
# first, make an empty list to put them into
all_words = []

# to hold the tags
tags = []

#########
patterns = []

# to hold the patterns and tags later on
xy = []

# loop through the json file, json file has 1 big intents, then it has tags, patterns and responses
for intent in intents['intents']:

    # figure out the tags and put them in the empty array
    tag = intent['tag']
    tags.append(tag)

    #############
    pattern = intent['patterns']
    patterns.append(pattern)

    # the patterns are also in an array, so a new loop has to be made
    for pattern in intent['patterns']:

        # patterns are things the user can say, now the first step begins: tokenization
        w = tokenize(pattern)

        # extend because w is an array, and I dont want arrays of arrays
        all_words.extend(w)

        # put into tokenized pattern and corresponding label
        xy.append((w, tag))

# to check
#print(all_words)



# exclude punctuations words
ignore_words = ['?', '!', '.', ',']
# and do the stemming process taken from other file, so lowercase words and chopped off words
all_words = [stem(w) for w in all_words if w not in ignore_words]

# now lets sort these words, and remove duplicate elements
# the sorted function will return a list in alphabetical order
all_words = sorted(set(all_words))
# also do with tags, not that necessary but still
tags = sorted(set(tags))

#print(all_words)



# now the words are tokenized and stemmed. The next step is bag of words

# list with X train data, which will contain the bag of words
X_train = []
# and Y, the tags, or associated number for each tags
y_train = []

# loop through the xy array, made above
for (pattern_sentence, tag) in xy:
    # calling the function bag of words, getting the tokenized sentence and all_words
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)

    # and for Y, for example, if tag is "delivery", it will give it label 0 and for other 1 and so on
    label = tags.index(tag)
    y_train.append(label) # class labele, CrossEntropyLoss later on


# convert to a numpy array
X_train = np.array(X_train)
y_train = np.array(y_train)




# create a new data set

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        # store the data
        self.x_data = X_train
        self.y_data = y_train

    # implement get item function
    #dataset[idx]
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # define length method
    def __len__(self):
        return self.n_samples

# Hyperparameters
batch_size = 8

# conclusion
dataset = ChatDataset()
# create a data loader
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

# by creating this dataSet and dataLoader it can automatically iterate and therefore get better training






# import and create the model with help from already model.py

hidden_size = 8
# number of different classes there are
output_size = len(tags)
# number of length of each pack of words that were created
input_size = len(X_train[0])

# to check if correct, it does
###print(input_size, len(all_words))
###print(output_size, tags)



# check if i have access to specific device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#model activation
model = NeuralNet(input_size, hidden_size, output_size).to(device)



# how intensely I want to train the data
# it was first 0.001
learning_rate = 0.001
num_epochs = 3000

# loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# training loop
for epoch in range(num_epochs):
    # use training loaders
    for (words, labels) in train_loader:
        # push to device
        words = words.to(device)
        labels = labels.to(device)

        # forward pass
        outputs = model(words)

        # calculate the loss
        loss = criterion(outputs, labels)

        # backward pass and optimizer steps
        # empty the gradients first
        optimizer.zero_grad()
        # calculate the back propagation
        loss.backward()
        optimizer.step()

        # this all is now the training loop
    
    # every 100th step, print the current epoch and which number of all epochs it is, and show the loss
    if (epoch+1) % 100 == 0:
        print(f'Epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')

# show the final results of loss, which will lower with each epoch for better results
# the lower the results, the better trained, the less difficult it was to train etc
print(f'final loss, loss={loss.item():.4f}')
 

# saving the data, create a dictonairy for the data
data = {
    
    # save different things
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags,
    #########
    "patterns": patterns,

}

# define a file name and serialize it
FILE = "data.pth"
# save the file
torch.save(data, FILE)
# to confirm
print(f'training complete. file saved to {FILE}')