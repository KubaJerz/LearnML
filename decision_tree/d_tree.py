from collections import Counter
import math
import numpy as np
from tree_node import TreeNode

class DecisionTree():

    def __init__(self, max_depth = 5, min_samples = 1, min_info_gain = 0.0) -> None:
        self.max_depth = max_depth #mac depth the tree can be
        self.min_samples = min_samples #min samples allowed in leaf for us to continues to split on it 
        self.min_info_gain = min_info_gain #min info gain needed to continue to build the tree


    def entrpoy(self, all_labels: list) -> float:
        class_prob = [label_count / len(all_labels) for label_count in Counter(all_labels).values()] #this well calc the prob each class being randomly setlected so len(set) = 10, five 0's, five 1's then class_prob = [.5,.5]
        return -1 * sum([p * math.log(p,2) for p in class_prob])
    

    '''
    This will return the sum weighted entropy for two lists
    '''
    def sets_entropy(self, splits: list) -> float:
        total = sum([len(split) for split in splits])
        return sum(len(split)/total * self.entrpoy(split) for split in splits) # we get the entropy of each split then weight it by its size compared to the total size of the splits then sum


    def split(self, data, f_index, threashold):
        bool_mask = data[:, f_index] < threashold #this makes array where for each row it 0 or 1 if if meet or did not the threashhold
        left = data[bool_mask]
        right = data[~bool_mask]
        return left, right

    '''
    We will take the greedy approach so,
    Given some data the best split will be on the feature that returns two sets with the lowest entrpoy.
    '''
    def find_best_split(self, data: np.array) -> tuple:
        
        b_s_entropy = float('inf')

        features_data = data[:, :-1] #last col is labels

        for f_idx in range(len(features_data[1])):
            f_values = features_data[:, f_idx] #all possibel values to split on
            f_values = np.unique(f_values) #we jsut make shure the values are all uniqine if not then only need to check one

            for possible_threashold in f_values: #now split on each featue and check if its good

                data_left, data_right = self.split(data, f_idx, possible_threashold)

                if len(data_left) > 0 and len(data_right) > 0:
                    split_entropy = self.sets_entropy([data_left[:, -1], data_right[:, -1]])#we send in two lists each of the labels of each side of the split and calcualte there sum entropy

                    if split_entropy < b_s_entropy: #the entropy of the set split we just found was better than all the other splits we have seen so far. 
                        b_s_entropy = split_entropy
                        data_right_best = data_right
                        data_left_best = data_left
                        best_f_idx = f_idx
                        best_f_val = possible_threashold

        return data_left_best, data_right_best, best_f_idx, best_f_val, b_s_entropy
    

    '''
    builds the tree by recursivly doing the best (greedy) split until one of the stopping conditions have been met 
    '''
    def build_tree(self, data: np.array, curr_depth: int) -> TreeNode:
        if curr_depth >= self.max_depth:
            return None
        
        s_data_left, s_data_right, s_f_idx, s_f_val, s_entropy = self.find_best_split(data) #find the ebst split and info form the split

        curr_entropy = self.entrpoy(data[:, -1]) #gets the entropy of the curr data 
        info_gain = curr_entropy - s_entropy #calc the information gain from the best split on this data

        node = TreeNode(data, s_f_idx, s_f_val, info_gain)

        if info_gain <= 0 or info_gain < self.min_info_gain:
            print('her info gain')
            return TreeNode(data, s_f_idx, s_f_val, info_gain)

        elif self.min_samples >= s_data_left.shape[0] or self.min_samples >= s_data_right.shape[0]:
            print('her min sampls')

            return TreeNode(data, s_f_idx, s_f_val, info_gain)
        
        curr_depth += 1
        node.left = self.build_tree(s_data_left, curr_depth)
        node.right = self.build_tree(s_data_right, curr_depth)

        return node
    
    '''
    trains the tree
    '''
    def fit(self, X_train: np.array, y_train: np.array):
        train_data = np.concatenate((X_train, np.reshape(y_train,(-1,1))),axis = 1)

        self.tree = self.build_tree(data=train_data, curr_depth=0)

    '''
    predicts for set samples
    '''
    def predict(self, X: np.array) -> np.array:
        preds = [self.predict_one_sample(x, self.tree) for x in X]
        return preds


    def predict_one_sample(self, x: np.array, tree: TreeNode) -> np.array:
        if tree.left == None and tree.right == None:
            return tree.label
        split_index = tree.f_idx
        if x[split_index] < tree.f_val:
            return self.predict_one_sample(x, tree.left)
        else:
            return self.predict_one_sample(x, tree.right)
        
        







                


