from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
from pruning import validation_accuracy
from random import sample
import numpy
from pruning import *
from copy import deepcopy

# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, pct):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''
    if pct == 0.0:
        return 0.0, 0.0
    dataSet = deepcopy(train_set)
    size = int(round((len(dataSet) * pct)))
    if size == 0:
        return 0.0, 0.0
    sub_set = sample(dataSet, size)
    tree = ID3(sub_set, attribute_metadata, deepcopy(numerical_splits_count), depth)
    accuracyOriginal = validation_accuracy(tree, validate_set)
    tree = reduced_error_pruning(tree,train_set,validate_set)
    accuracyPruned = validation_accuracy(tree, validate_set)
    return accuracyOriginal, accuracyPruned

def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, pcts):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''

    sumValueOriginal = 0.0
    sumValuePruned = 0.0
    for _ in range(iterations):
        accuracyOriginal, accuracyPruned = get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, pcts)
        sumValueOriginal += accuracyOriginal
        sumValuePruned += accuracyPruned
    averageOriginalAccuracy = sumValueOriginal / iterations
    averagePrunedAccuracy = sumValuePruned / iterations

    return averageOriginalAccuracy, averagePrunedAccuracy



# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''
    pcts = numpy.linspace(lower, upper, int((upper - lower) / increment) + 1).tolist()
    data = []
    dataPruned = []
    for i in range(len(pcts)):
        averageOriginalAccuracy, averagePrunedAccuracy = get_graph_data(train_set,attribute_metadata, validate_set, numerical_splits_count, depth, iterations, pcts[i])
        data.append(averageOriginalAccuracy)
        dataPruned.append(averagePrunedAccuracy)
    plt.plot(pcts, data, 'r-o', label='Original Tree')
    plt.plot(pcts, dataPruned, 'b-*', label='Pruned Tree')
    plt.xlabel('Perncentage of Training Data')
    plt.ylabel('Accuracy on Validation Data')
    plt.title('Decision Tree Learning Curve')
    plt.legend(loc=4)
    plt.savefig('output/curve.png')

