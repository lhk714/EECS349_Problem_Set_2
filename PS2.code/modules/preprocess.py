import math
from node import Node
import sys

def preprocess(data_set, attribute_metadata):
    for item in attribute_metadata:
        itemIndex = attribute_metadata.index(item)

        if item['is_nominal']:  # calculate mode

            dictionary = {}
            maxCount = -1
            modeValue = None

            for data in data_set:
                key = data[itemIndex]
                if key == None or key == '?':
                    continue
                if dictionary.has_key(key):
                    dictionary[key] += 1
                else:
                    dictionary[key] = 1
            for key, value in dictionary.items():
                if value > maxCount:
                    modeValue = key
                    maxCount = value
            for data in data_set:
                if data[itemIndex] == None or data[itemIndex] == '?':
                    data[itemIndex] = modeValue

        else: # calculate average

            sumValue = 0.0
            averageValue = 0.0
            numOfKnown = 0
            for data in data_set:
                key = data[itemIndex]
                if key == key == None or key == '?':
                    continue
                sumValue += key
                numOfKnown += 1
            if numOfKnown == 0:
                averageValue = 0.0
            else:
                averageValue = float(sumValue) / numOfKnown
            for data in data_set:
                if data[itemIndex] == None or data[itemIndex] == '?':
                    data[itemIndex] = averageValue

    return data_set
