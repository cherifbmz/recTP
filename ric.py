from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.metrics import accuracy_score

def initialize(dimentions):
    parameters={}
    C=len (dimentions)
    for c in range(1,C):
        parameters['W'+str(c)]=np.random.randn(dimentions[c],dimentions[c-1])
        parameters["b"+str(c)]=np.random.randn(dimentions[c],1)

    return parameters

def sigmoid(Z):
        return 1/(1+np.exp(-Z))


def forward_propagation(X,paramaters):
    activation={"A0":X}
    C=len(paramaters)//2

    for c in range(1,C+1):
      Z=paramaters["W"+str(c)].dot(activation["A"+str(c-1)])+paramaters["b"+str(c)]
      activation["A"+str(c)]=sigmoid(Z)

    return activation



def function_cout(A, y):
    m = y.shape[1]
    return (-1 / m) * np.sum(y * np.log(A) + (1 - y) * np.log(1 - A))

def back_propagation(y,activations,paramaters):
    m=y.shape[1]
    C=len(paramaters)//2

    dZ=activations['A'+str(C)]-y
    gradients={}
    for c in reversed((range(1,C+1))):
        gradients["dW"+str(c)]=1/m*np.dot(dZ,activations["A"+str(c-1)].T)
        gradients["db"+str(c)]=1/m*np.sum(dZ,axis=1,keepdims=True )
        if c>1:
            dZ=np.dot(paramaters["W"+str(c)].T,dZ)*activations["A"+str(c-1)]*(1-activations["A"+str(c-1)])
   


    return gradients

def update_parameters(gradients,parameters,learning_rate):
    C=len(parameters)//2
     
    for c in range(1,C+1):
        parameters["W"+str(c)]=parameters["W"+str(c)]-learning_rate*gradients["dW"+str(c)]
        parameters["b"+str(c)]=parameters["b"+str(c)]-learning_rate*gradients["db"+str(c)] 

    return parameters

def predict(X, parameters):
    activations = forward_propagation(X, parameters)
    C = len(parameters) // 2
    return (activations['A' + str(C)] > 0.5).astype(int)

def train_mlp(X, y, hidden_layers, learning_rate=0.1, n_iter=1000):
    np.random.seed(0)
    dimensions = list(hidden_layers)
    dimensions.insert(0, X.shape[0])
    dimensions.append(y.shape[0])
    parameters = initialize(dimensions)
    train_loss = []
    train_acc = []
    for i in tqdm(range(n_iter)):
        activations = forward_propagation(X, parameters)
        gradients = back_propagation(y, activations, parameters)
        parameters = update_parameters(gradients, parameters, learning_rate)
        if i % 10 == 0:
            C = len(parameters) // 2
            train_loss.append(function_cout(activations['A' + str(C)], y))
            y_pred = predict(X, parameters)
            train_acc.append(accuracy_score(y.flatten(), y_pred.flatten()))
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))
    ax[0].plot(train_loss, label='Train Loss')
    ax[0].legend()
    ax[1].plot(train_acc, label='Train Accuracy')
    ax[1].legend()
    plt.show()
    return parameters
    

X = np.array([[0, 0, 1, 1], [0, 1, 0, 1]])
y = np.array([[0, 1, 1, 0]])
parameters = train_mlp(X, y, hidden_layers=(4, 4), learning_rate=0.1, n_iter=5000)
y_pred= predict(X, parameters)
print("Predictions:", y_pred.flatten())
print("Actual:", y.flatten())
print("Accuracy:", accuracy_score(y.flatten(), y_pred.flatten()))
