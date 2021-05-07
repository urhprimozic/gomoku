import torch.nn as nn
import torch
import torch.optim as optimizer
import torch.nn.functional as F
'''
input : (15x15) numpy array
output : realno število ??
'''
class NNPolicy(nn.Module):
    """
    Returns a fully connected neural network of 
    given dimensions. The input is of dimensions
    of the shape of the observations and output
    is of the shape of number of actions.

    TODO: fully connected je za en kurac, k js hočem threadse gledat
    """

    def __init__(self, sizes, activation=nn.ReLU(inplace=True), output_activation=None):
        super(NNPolicy, self).__init__()
        layers = []
        for i in range(len(sizes) - 1):
            layers.append(nn.Linear(sizes[i], sizes[i+1]))
            if i < len(sizes) - 2:
                layers.append(activation)
        self.fwd = nn.Sequential(*layers)
    
    def forward(self, x):
        return F.softmax(self.fwd(x), dim=-1)



class EncodingNNPolicy():
    '''
    Varianta Encoding +  NN
    Ideja za Learning: Policy gradients za NN, hyperopt+hyper_optimisation.py za parametre
    '''
    def __init__(self) -> None:
        self.nn = NNPolicy([255, 100, 1])
        # already calculated potentials
        self.memory = []
    

def train():
    return NotImplementedError

if __name__ == '__main__':
    raise NotImplementedError