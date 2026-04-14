import numpy as np

class NeuralNetwork:
    # initialize a list of weights matrices; store network architecture and learning rate
    def __init__(self, layers, alpha=0.1):
        
        self.W = [] # weight list object
        self.layers = layers # a list of integers representing arch of feedforward network
        self.alpha = alpha   # specifies learning rate (applied during weight update phase)

        # start looping from the index of the first layer; stop before reaching the last two layers
        for i in np.arange(0, len(layers) - 2):
            # randomly initialize a weight matrix 
            # clever trick: the bias is handled as an extra node!
            w = np.random.randn(layers[i] + 1, layers[i + 1] + 1) # current layer + next layer + bias
            self.W.append(w / np.sqrt(layers[i])) # normalize variance
            
        # handle case where connections need a bias term but the output does not
        w = np.random.randn(layers[-2] + 1, layers[-1])
        self.W.append(w / np.sqrt(layers[-2]))

    def __repr__(self):
        # debugging: return string representing structure. Not called unless specified
        return "NeuralNetwork: {}".format(
            "-".join(str(l) for l in self.layers))

    def sigmoid(self, x):
        # compute and return the sigmoid activation value for a given input value
        return 1.0 / (1 + np.exp(-x))

    def sigmoid_deriv(self, x):
        # compute the derivative of the sigmoid function ASSUMING that x has already been passed through sigmoid
        return x * (1 - x)

    def fit(self, X, y, epochs=1000, displayUpdate=100):
        # insert a column of 1's as the last entry in the feature; allows bias to be treated as trainable parameter
        X = np.c_[X, np.ones((X.shape[0]))]

        # loop over the desired number of epochs
        for epoch in np.arange(0, epochs):
            # loop over each individual data point and train network
            for (x, target) in zip(X, y):
                self.fit_partial(x, target)

            # output limiter: check to see if update should be printed
            if epoch == 0 or (epoch + 1) % displayUpdate == 0:
                loss = self.calculate_loss(X, y)
                print("[INFO] epoch={}, loss={:.7f}".format(
                    epoch + 1, loss))

    def fit_partial(self, x, y):
        # construct a list of output activations for each layer
        
        A = [np.atleast_2d(x)] # initialize the feature vector (2D numpy array)

        # FEEDFORWARD:
        # loop over the layers in the network
        for layer in np.arange(0, len(self.W)):
            # generate net input by taking the dot product between activation (current layer) 
            # and weight matrix (self.W[layer])
            net = A[layer].dot(self.W[layer])
            
            # apply sigmoid activation function to net input, generating net output
            out = self.sigmoid(net)
            
            # append output to feature vector (basically output array)
            A.append(out)

        # BACKPROPAGATION:
        
        # step 1. compute the difference between "prediction" (last item in net output vector)
        # and the true target value (stored in 'y')
        error = A[-1] - y

        # step 2. apply "chain rule" i.e. compute the error times the derivitive of sigmoid for each output value
        D = [error * self.sigmoid_deriv(A[-1])]

        # step 3. iterate over the layers backwards, sans the last two that are already covered
        for layer in np.arange(len(A) - 2, 0, -1):
            # find the delta, which is equal to the delta of the previous layer dotted with the weight
            # matrix of the current layer, TIMES the sigmoid derivative of the current layer. 
            # Another reason we start on 3rd-to-last item
            delta = D[-1].dot(self.W[layer].T) 
            delta = delta * self.sigmoid_deriv(A[layer])
            
            # append results to an array of deltas
            D.append(delta)

        # flip the whole list back around so it's ordered first-to-last again for the next phase
        D = D[::-1]

        # WEIGHT UPDATE PHASE: 
        # this is the real sauce. Update the weights (i.e. "teach" them) by dotting the layer activations (A) 
        # with their deltas (D), then multipying that by the "learning rate" set at
        # module call (alpha = [learning rate])
        # This basically "adjusts the dials" for each node to make their outputs 
        # closer to what we expect (the 'y' value)
        for layer in np.arange(0, len(self.W)):
            self.W[layer] += -self.alpha * A[layer].T.dot(D[layer])

    def predict(self, X, addBias=True):
        # initialize the output prediction 'p' as the input features. Recall that 'X' is defined in fit()
        # this will be forward propagated through the network to finalize prediciton
        p = np.atleast_2d(X) 

        # check to see if the bias column should be added (default TRUE on first epoch)
        if addBias:
             # insert a column of 1's as the last entry in the feature matrix (bias)
             p = np.c_[p, np.ones((p.shape[0]))]

        # loop over our layers in the network
        for layer in np.arange(0, len(self.W)):
            # compute the output prediction, which is the dotting the current activation value 'p' 
            # with the weight matrix of the current layer, and then passing that value to sigmoid
            p = self.sigmoid(np.dot(p, self.W[layer]))

        # return the predicted value
        return p

    def calculate_loss(self, X, targets):
        # make predictions for the input data points then compute the loss (i.e. how much learning is left)
        targets = np.atleast_2d(targets)
        predictions = self.predict(X, addBias=False)
        loss = 0.5 * np.sum((predictions - targets) ** 2)

        # return the loss
        return loss
