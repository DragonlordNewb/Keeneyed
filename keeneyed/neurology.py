from math import exp
from random import random, seed
from time import time

seed(time())

def randomFloat():
    return (random()*2) - 1

def sigmoid(x):
    return 1 / (1 + exp(-x))

def sigdrvt(x):
    return sigmoid(x)*(1-sigmoid(x))

class FeedforwardNeuralNetworkLayer:

    def __init__(self, input_size: int, output_size: int, learning_rate: float) -> None:
        self.input_size = input_size
        self.input_vector = None
        self.output_size = output_size
        self.output_vector = None
        self.learning_rate = learning_rate
        self.weights = [[randomFloat() for _ in range(input_size)] for _ in range(output_size)]
        self.biases = [randomFloat() for _ in range(output_size)]

    def forward(self, vector: list[float]) -> list[float]:
        self.input_vector = vector
        outputs = [
            sum(self.weights[i][j] * vector[j] for j in range(self.input_size)) + self.biases[i]
            for i in range(self.output_size)
        ]
        self.output_vector = [sigmoid(x) for x in outputs]
        return self.output_vector
    
    def backward(self, error: list[float]) -> list[float]:
        outputs = [
            sum(self.weights[i][j] * self.input_vector[j] for j in range(self.input_size)) + self.biases[i]
            for i in range(self.output_size)
        ]
        deltas = [error[i] * sigdrvt(outputs[i]) for i in range(self.output_size)]
        for i in range(self.output_size):
            for j in range(self.input_size):
                self.weights[i][j] -= self.learning_rate * deltas[i] * self.input_vector[j]
            self.biases[i] -= self.learning_rate * deltas[i]
        prev_error = [0.0 for _ in range(self.input_size)]
        for j in range(self.input_size):
            for i in range(self.output_size):
                prev_error[j] += deltas[i] * self.weights[i][j]
        return prev_error

FNNL = FeedforwardNeuralNetworkLayer

class FeedforwardNeuralNetwork:

    def __init__(self, learning_rate, *layer_sizes: list[int]) -> None:
        self.layers = []
        self.layer_sizes = layer_sizes
        for i in range(len(layer_sizes) - 1):
            self.layers.append(
                FeedforwardNeuralNetworkLayer(layer_sizes[i], layer_sizes[i+1], learning_rate)
            )

    def __iter__(self):
        return iter(self.layers)
    
    def reverse(self):
        return iter(self.layers[::-1])

    def forward(self, vector: list[float]) -> list[float]:
        for layer in self:
            vector = layer.forward(vector)
        return vector
    
    def backward(self, error: list[float]) -> list[float]:
        for layer in self.reverse():
            error = layer.backward(error)
        return error
    
    def train_single(self, input: list[float], target: list[float]) -> list[float]:
        prediction = self.forward(input)
        error = [prediction[i] - target[i] for i in range(len(target))]
        return self.backward(error)
    
    def train(self, inputs, targets, epochs: int) -> list[list[float]]

FNN = FeedforwardNeuralNetwork

if __name__ == "__main__":
    fnn = FNN(0.01, 2, 3, 3, 1)
    print(fnn.forward([1, 0]))