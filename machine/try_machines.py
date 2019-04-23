#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

df = pd.read_csv('./../data/tidy_data.csv', index_col=0, header=0)
df = df[pd.notnull(df['time_created'])]
data_name = ['num_followers',
             'num_following',
             'num_repos',
             'days_created',
             'days_updated'
             ]
data = df.loc[:, data_name]
target = df.loc[:, 'pull_request'].values

data_training, data_test, target_training, target_test = \
        train_test_split(data, target, test_size=0.2, random_state=1)

# K nearest neighors ----------------------------------------------------------
# knn = KNeighborsClassifier(n_neighbors=2)
# knn.fit(data_training, target_training)
# predictions = knn.predict(data_test)
# print(accuracy_score(target_test, predictions))
# print(sum(target_test))
# print(sum(predictions))

# decision tree ---------------------------------------------------------------
# decision_tree_machine = tree.DecisionTreeClassifier(criterion='gini')
# decision_tree_machine.fit(data_training, target_training)
# predictions = decision_tree_machine.predict(data_test)
# print(accuracy_score(target_test, predictions))
#
# cmatrix = pd.DataFrame(
#     confusion_matrix(target_test, predictions),
#     columns = ['Predict 0', 'Predict 1', 'Predict 2', 'Predict 3'],
#     index = ['True 0', 'True 1', 'True 2', 'True 3']
# )
#
# print(cmatrix)
#
# np.max(predictions)
# np.max(target_test)

# logist ----------------------------------------------------------------------
# the probability of submitting a pull request
print(sum(target) / len(target))
# 0.005531084192611873
