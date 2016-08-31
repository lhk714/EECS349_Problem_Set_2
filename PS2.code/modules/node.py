# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 if numeric and a dictionary if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on

import random


class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None
        self.mode = None # backup the label if the node is pruned

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''

        # for instance[self.decision_attribute] is unknown, assign a random branch

        if self.label != None: # it is a leaf node
            return self.label
        else:
            if self.is_nominal ==  True:
                if instance[self.decision_attribute] == None or instance[self.decision_attribute] == '?':
                    matchingChildren = self.children[random.choice(self.children.keys())]
                elif not instance[self.decision_attribute] in self.children.keys():
                    matchingChildren = self.children[random.choice(self.children.keys())]
                else:
                    matchingChildren = self.children[instance[self.decision_attribute]]
            else:
                if instance[self.decision_attribute] == None or instance[self.decision_attribute] == '?':
                    matchingChildren = self.children[random.randint(0,1)]
                else:
                    matchingChildren = self.children[0] if instance[self.decision_attribute] < self.splitting_value else self.children[1]
        return matchingChildren.classify(instance)

    def print_tree(self, indent=0):
        '''
        returns a string of the entire tree in human readable form
        '''
        # Your code here
        return (self.printTreeHelp(self,indent))


    def printTreeHelp(self,node,indent = 0):
        string = "|   " * indent

        if node.label != None:
            return string + "--> " + str(node.label) + "\n"
        elif node.is_nominal == True:
            s = ''
            for key,value in node.children.items():
                string += s + (str(node.name) + " = " + str(key) + "\n" + node.printTreeHelp(value, indent + 1))
                s = "|   " * indent
            return string
        elif node.splitting_value != None:
            sign = [" < ", " >= "]
            s = ''
            for key,value in node.children.items():
                string += s + str(node.name) + sign[key] + str(node.splitting_value) + "\n" + node.printTreeHelp(value, indent + 1)
                s = "|   " * indent
            return string
        else:
            return ''


    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        string = self.printDNFTreeHelp(self,[])
        dnfTree = string[0]
        flag = True
        for i in range(1,len(string)-1):
            if string[i] == '(' or string[i] == ')':
                dnfTree += string[i]
                flag = True
            elif string[i] == '|':
                dnfTree += " OR\n"
                flag = True
            elif string[i] == '!':
                dnfTree += " --> "
                flag = True
            else:
                if flag:
                    dnfTree += str(string[i])
                else:
                    dnfTree += " AND " + str(string[i])
                flag = False
        dnfTree += "\n"
        return dnfTree

    def printDNFTreeHelp(self,node,s = []):
        if node.label != None:
            return ['('] + s + ['!'] + [node.label] + [')'] + ['|']
        elif node.is_nominal == True:
            string = []
            for key,value in node.children.items():
                string += node.printDNFTreeHelp(value, s + [str(node.name) + " = " + str(key)])
            return string
        elif node.splitting_value != None:
            string = []
            sign = [" < ", " >= "]
            for key,value in node.children.items():
                string += node.printDNFTreeHelp(value, s + [str(node.name) + sign[key] + str(node.splitting_value)])
            return string
        else:
            return ['('] + s + [')'] + ['|']







