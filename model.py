import torch
import torch.nn as nn

# this will be a feed-forward neural net with two hidden layers
# see as in the photo, input layers, number of classes as output
# then after, applying the softmax to get probabilities for each classes
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):

        super(NeuralNet, self).__init__()

        # creating three linear layers
        # input and classes are fixed, but amount of hidden size can be made up
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)

        # activation function for in between
        self.relu = nn.ReLU()

    # implement the forward pass
    def forward(self, x):
        out = self.l1(x)
        # apply activation function
        out = self.relu(out)

        # then repeat two more times
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax
        return out
