import math
from node import Node
from preprocess import *
import sys
from copy import deepcopy

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    # Your code here
    data_set = preprocess(data_set, attribute_metadata) # preprocess the data_set, substitude unkown with mode if nominal, with average if numerical

    return ID3Helper(data_set, attribute_metadata, numerical_splits_count, depth)

def ID3Helper(data_set, attribute_metadata, numerical_splits_count, depth):
    '''the main function of ID3'''
    node = Node()
    if not data_set:
        node.label = None
    else:
        node.mode = mode(data_set) # backup the label if the node is pruned

    if depth == 0:
        node.label = mode(data_set)  # node should output a label
    elif check_homogenous(data_set) != None:  # all the data in data_set are the same, no need to split
        node.label = check_homogenous(data_set)
    elif not attribute_metadata:
        node.label = mode(data_set)
    else:
        attribute, splitValue = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
        if attribute == False and splitValue == False:  # If gain ratio of all the attributes is 0, return node with label = mode(data_set)
            node.label = mode(data_set)
            return node

        node.decision_attribute = attribute
        node.name = attribute_metadata[attribute]['name']
        node.is_nominal = attribute_metadata[attribute]['is_nominal']
        node.splitting_value = splitValue
        children = {}
        depth -= 1  # Whenever there is a node generated, if depth >0, then depth--

        if node.is_nominal == True:
            splitDictionary = split_on_nominal(data_set, attribute)
            for key, value in splitDictionary.items():
                children[key] = ID3Helper(value, attribute_metadata, numerical_splits_count, depth)
        else:
            if numerical_splits_count[attribute] == 0:
                node.label = mode(data_set)
                return node
            else:
                new_splits_count = deepcopy(numerical_splits_count)
                new_splits_count[attribute] -= 1
                splitDictionary1, splitDictionary2 = split_on_numerical(data_set, attribute, splitValue)
                children[0] = ID3Helper(splitDictionary1, attribute_metadata, new_splits_count, depth)
                children[1] = ID3Helper(splitDictionary2, attribute_metadata, new_splits_count, depth)
        node.children = children
    return node


def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
    '''
    # Your code here
    if data_set == None:
        return None

    # Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    for element in data_set:
        if element[0] != data_set[0][0]:
            return None
    return data_set[0][0]
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    # Your code here

    maxGainRatio = 0.0
    bestAttribute = False
    splitValue = None

    for attribute in range(1, len(attribute_metadata)):
        if attribute_metadata[attribute]['is_nominal']:
            gainRatio = gain_ratio_nominal(data_set, attribute)
            numericalSplit = None
        else:
            numericalStepSize = 1  # default step size
            gainRatio, numericalSplit  = gain_ratio_numeric(data_set, attribute, numericalStepSize)  # default step size

        if gainRatio > maxGainRatio:
            maxGainRatio = gainRatio
            bestAttribute = attribute
            splitValue = numericalSplit

    if maxGainRatio == 0.0:
        return False, False
    elif attribute_metadata[bestAttribute]['is_nominal']:
        return bestAttribute, False
    else:
        if numerical_splits_count[bestAttribute] == 0:
            return False, False
        else:
            return bestAttribute, splitValue



# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])
def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    # Your code here
    dictionary = {}  # save the count # for each distinct element
    label = None # mode label
    maxCount = -1

    #  count # for each distinct element
    for element in data_set:
        key = element[0]
        if key in dictionary.keys():
            dictionary[key] += 1
        else:
            dictionary[key] = 1

    #  calculate mode
    for key, value in dictionary.items():
        if value > maxCount:
            label = key
            maxCount = value

    return label
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    numOfElements = len(data_set)  # count the total # of elements in data_set
    dictionary = {}  # save the count # for each distinct element
    entropyResult = 0.0  # entropy output result
    #  count # for each distinct element
    for element in data_set:
        label = element[0]
        if label in dictionary.keys():
            dictionary[label] += 1
        else:
            dictionary[label] = 1

    #  calculate entropy
    for _, value in dictionary.items():
        p = float(value) / numOfElements
        if p == 0.0:
            entropyResult = 0.0
        else:
            entropyResult -= p * math.log(p,2)
    return entropyResult

# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    # Your code here
    numOfElements = len(data_set)

    igIntermedia = 0.0
    ivIntermedia = 0.0

    dictionary = split_on_nominal(data_set, attribute)

    for key,value in dictionary.items():
        portionRatio = float(len(value)) / numOfElements
        igIntermedia += portionRatio * entropy(value)
        ivIntermedia += portionRatio * math.log(portionRatio,2)

    informationGain = entropy(data_set) - igIntermedia
    intrinsicValue = - ivIntermedia
    if intrinsicValue == 0.0: # ensure denominater != 0
        informationGainRatio = 0.0
    else:
        informationGainRatio = informationGain/intrinsicValue

    return informationGainRatio
# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps = 1):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    # Your code here
    numOfElements = len(data_set)
    informationGainRatio = 0.0
    threshold = 0.0

    for i in range(0,len(data_set),steps):
        th = data_set[i][attribute]
        portion1,portion2 = split_on_numerical(data_set,attribute,th)
        if len(portion1) != 0 and len(portion2) != 0:
            portion1Ratio = float(len(portion1)) / numOfElements
            portion2Ratio = float(len(portion2)) / numOfElements
            informationGain = entropy(data_set) - portion1Ratio * entropy(portion1) - portion2Ratio * entropy(portion2)
            intrinsicValue = - portion1Ratio * math.log(portion1Ratio, 2) - portion2Ratio * math.log(portion2Ratio,2)
            if intrinsicValue != 0 and informationGain / intrinsicValue > informationGainRatio:
                informationGainRatio = informationGain / intrinsicValue
                threshold = th
    return informationGainRatio, threshold
# ======== Test case =============================
# data_set,attr,step = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [1,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    # Your code here
    dictionary = {}

    for element in data_set:
        key = element[attribute]
        if key in dictionary.keys():
            dictionary[key].append(element)
        else:
            dictionary[key] = [element]

    return dictionary
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    # Your code here
    dictionary1 = []
    dictionary2 = []
    for element in data_set:
        if element[attribute] < splitting_value:
            dictionary1.append(element)
        else:
            dictionary2.append(element)
    return dictionary1, dictionary2
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
