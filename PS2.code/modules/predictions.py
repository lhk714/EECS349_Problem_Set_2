import os.path
from operator import xor
from parse import *

# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''

    with open('./output/predictions.csv', 'w+') as cursor:
        writer = csv.writer(cursor)
        fieldnames = ['winpercent', ' oppwinpercent', ' weather', ' temperature', ' numinjured',' oppnuminjured',
                  ' startingpitcher', ' oppstartingpitcher', ' dayssincegame', ' oppdayssincegame', ' homeaway', ' rundifferential', ' opprundifferential', ' winner']
        writer.writerow(fieldnames)
        predict_set, _ = parse(predict, True)
        for item in predict_set:
            item[0] = tree.classify(item)
            for i in range(1, len(item)):
                if item[i] == None:
                    item[i] = '?'
            item = collections.deque(item)
            item.rotate(-1)
        writer.writerows(predict_set)