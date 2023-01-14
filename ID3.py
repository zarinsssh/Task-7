import os
import pandas as pd
import numpy as np

def CalcTotalEntropy(train_data, label, class_list):
    
    total_row = train_data.shape[0]
    total_entr = 0

    for c in class_list:
        total_class_count = train_data[train_data[label] == c].shape[0]
        total_class_entr = -(total_class_count/total_row)*np.log2(total_class_count/total_row)
        total_entr += total_class_entr

    return total_entr

def CalcEntropy(feature_value_data, label, class_list):
    class_count = feature_value_data.shape[0]
    entropy = 0

    for c in class_list:
        label_class_count = feature_value_data[feature_value_data[label] == c].shape[0]
        entropy_class = 0
        if label_class_count != 0:
            probability_class = label_class_count/class_count
            entropy_class = - probability_class * np.log2(probability_class)
        entropy += entropy_class
    
    return entropy

def CalcInfoGain(feature_name, train_data, label, class_list):
    feature_value_list = train_data[feature_name].unique()
    total_row = train_data.shape[0]
    feature_info = 0.0

    for feature_value in feature_value_list:
        feature_value_data = train_data[train_data[feature_name] == feature_value]
        feature_value_count = feature_value_data.shape[0]
        feature_value_entropy = CalcEntropy(feature_value_data, label, class_list)
        feature_value_probability = feature_value_count/total_row
        feature_info += feature_value_probability * feature_value_entropy

    return CalcTotalEntropy(train_data, label, class_list) - feature_info

def FindMostInformativeFeature(train_data, label, class_list):
    feature_list = train_data.columns.drop(label)
    max_info_gain = -1
    max_info_feature = None

    for feature in feature_list:
        feature_info_gain = CalcInfoGain(feature, train_data, label, class_list)
        if max_info_gain < feature_info_gain:
            max_info_gain = feature_info_gain
            max_info_feature = feature
    
    return max_info_feature

def GenerateSubTree(feature_name, train_data, label, class_list):
    feature_value_count_dict = train_data[feature_name].value_counts(sort=False)
    tree = {}

    for feature_value, count in feature_value_count_dict.items():
        feature_value_data = train_data[train_data[feature_name] == feature_value]

        assigned_to_node = False
        for c in class_list:
            class_count = feature_value_data[feature_value_data[label] == c].shape[0]
            
            if class_count == count:
                tree[feature_value] = c
                train_data = train_data[train_data[feature_name] != feature_value]
                assigned_to_node = True
        if not assigned_to_node:
            tree[feature_value] = "?"
    
    return tree, train_data

def MakeTree(root, prev_feature_value, train_data, label, class_list):
    print(train_data.shape[0])
    
    if train_data.shape[0] != 0:
        max_info_feature = FindMostInformativeFeature(train_data, label, class_list)
        tree, train_data = GenerateSubTree(max_info_feature, train_data, label, class_list)
        next_root = None
        
        if prev_feature_value != None:
            root[prev_feature_value] = dict()
            root[prev_feature_value][max_info_feature] = tree
            next_root = root[prev_feature_value][max_info_feature]
        else:
            root[max_info_feature] = tree
            next_root = root[max_info_feature]
        
        for node, branch in list(next_root.items()):
            if branch == "?":
                feature_value_data = train_data[train_data[max_info_feature] == node]
                MakeTree(next_root, node, feature_value_data, label, class_list)

def Id3(train_data_m, label):
    train_data = train_data_m.copy()
    tree = {}
    class_list = train_data[label].unique()
    MakeTree(tree, None, train_data, label, class_list)

    return tree


def Predict(tree, instance):
    if not isinstance(tree, dict):
        return tree 
    else:
        root_node = next(iter(tree)) 
        feature_value = instance[root_node] 
        if feature_value in tree[root_node]: 
            return Predict(tree[root_node][feature_value], instance)
        else:
            return None

def Evaluate(tree, test_data_m, label):
    correct_preditct = 0
    wrong_preditct = 0
    for index, row in test_data_m.iterrows(): 
        result = Predict(tree, test_data_m.iloc[index]) 
        if result == test_data_m[label].iloc[index]: 
            correct_preditct += 1 
        else:
            wrong_preditct += 1 
    accuracy = correct_preditct / (correct_preditct + wrong_preditct) 

    return accuracy

def main():
    df_path = os.path.join(os.path.dirname(__file__), "SDN_traffic.csv")

    train_data_m = pd.read_csv(df_path)

    tree = Id3(train_data_m, 'category')

    print(tree)

if __name__ == "__main__":
    main()
