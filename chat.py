import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

count = 0

# check if i have access to specific device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# open the file with intents
with open('intents5.json', 'r') as f:
    intents = json.load(f)

# open the file with saved data
FILE = "data.pth"

# since data was saved in train.py, now just load the data
data = torch.load(FILE)


# get the same information, get the information to create the model
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]


#model activation
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# load the state dict of the creation
# now it knows the learned parameters
model.load_state_dict(model_state)

# set to evaluation mode
model.eval()



# implement the actual chat

# give bot a name
bot_name = "Laura"


# define a function that gets a message as parameter and then returns the response
def get_response(msg):

    # first tokenize the sentence and then calculate a bag of words, just like the training data
    # tokenize the message
    sentence = tokenize(msg)
    # create bag of words
    X = bag_of_words(sentence, all_words)
    # reshape it, give it 1 roll cause there is only one sample, 0 as the number of columns
    X = X.reshape(1, X.shape[0])
    # convert to torch, numpy because bag of words returns in a numpy array
    X = torch.from_numpy(X)

    # to get the predictions
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    # the class label, the number
    tag = tags[predicted.item()]

    # apply softmax
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # the probability is large enough
    # first it was 0.75
    if prob.item() > 0.75:

        # find the corresponding intent, loop through all intents and check if tag matches
        for intent in intents["intents"]:

            if tag == intent["tag"]:

                if tag == "fruit":
                    global count
                    count = count + 1
                    print(count)

                if count == 3:
                    #return random.choice(intent['responses']), "fruit gamification activated"
                    return f"{random.choice(intent['responses'])} "" Your fruit gamification pack is now activated"

                # choose a random response from the bot to say
                return random.choice(intent['responses'])

                # if the user says something specifc, the chatbot will remember it
                ###################!!!!!!
                ##if tag == "funny":
                ##    count = count + 1
                ##    print("joke has reached: ", count, ". The leaderboard gamification packet is now active")

                # perhaps for later, if count is 3 then interface changes. Or if count is 3
                # then another intens.json will be used that is more funny based.
                # how to make more data-driven?


    # if not large enough
    return "I do not understand. Could you perhaps rephrase it with some more words? :)"

