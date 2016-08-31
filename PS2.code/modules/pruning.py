from node import Node
from ID3 import *
from operator import xor
from copy import deepcopy
from random import sample

# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(root,training_set,validation_set): # greedy first search
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    '''
    tree = deepcopy(root)
    accuracy, newTree = pruning(tree, training_set, validation_set)
    return newTree

def pruning(tree, training_set, validation_set):  # recursive greedy first search
    originalAccuracy = validation_accuracy(tree, validation_set)

    newTree = deepcopy(tree)  # made a new tree
    nodeDictionary = breadth_first_search(newTree, [newTree])
    numOfNode = len(nodeDictionary)
    pruneAccuracy = []
    for i in range(numOfNode):
        dictionary = deepcopy(nodeDictionary)
        prune_node(dictionary[i])
        pruneAccuracy.append(validation_accuracy(dictionary[0], validation_set)) #dictionary[0] = root

    maxAccuracy = max(pruneAccuracy)
    maxAccuracyIndex = pruneAccuracy.index(maxAccuracy)

    if maxAccuracy > originalAccuracy:
        prune_node(nodeDictionary[maxAccuracyIndex])
        return  pruning(newTree, training_set, validation_set)
    else:
        return originalAccuracy, tree



def breadth_first_search(root, dictionary):
    '''given the root node, will complete a breadth-first-search on the tree, returning the value of each node in the correct order'''
    if root.label != None:
        return dictionary
    else:
        children = get_children(root)
        dictionary += children
        for item in children:
            dictionary = breadth_first_search(item, dictionary)
        return dictionary

def get_children(node):
    dictionary = []
    if node.label != None:
        return dictionary
    for _, value in node.children.items():
        if value.label == None:
            dictionary.append(value)
    return dictionary

def prune_node(node):

    node.label = node.mode
    node.decision_attribute = None
    node.is_nominal = None
    node.value = None
    node.splitting_value = None
    node.children = {}
    node.name = None



def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    # Your code here
    numOfCorrect = 0
    validationSize = len(validation_set)
    if tree and validationSize > 0:
        for sample in validation_set:
            if tree.classify(sample) == sample[0]:
                numOfCorrect += 1
        return float(numOfCorrect)/validationSize
    else:
        return 0.0

