'''
Try different machines
'''

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# from sklearn.neighbors import KNeighborsClassifier
# from sklearn import tree
import os
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import numpy as np
import pandas as pd

df = pd.read_csv(
    '/home/guanghua/Documents/clemson/courses/9000_Machine_Learning/ECON900_ps1/data/tidy_data.csv',
    index_col=0,
    header=0
)

df = df[pd.notnull(df['time_created'])]
data_name = ['num_followers',
             'num_following',
             'num_repos',
             'days_created',
             'days_updated'
             ]
data = df.loc[:, data_name]
data['days_created_sign'] = np.sign(data['days_created'])
data['days_updated_sign'] = np.sign(data['days_updated'])
data['num_followers_pos'] = (data['num_followers'] > 0) * 1
data['num_following_pos'] = (data['num_following'] > 0) * 1
data['num_repos_pos'] = (data['num_repos'] > 0) * 1
target = df.loc[:, 'pull_request'].values

data_training, data_test, target_training, target_test = \
        train_test_split(data, target, test_size=0.90, random_state=23042019)

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

# logistic --------------------------------------------------------------------
## the probability of submitting a pull request
#print(sum(target) / len(target))
## 0.005531084192611873
#
logistic_machine = LogisticRegression(
    random_state=23042019,
    C=1.0,
    tol=1e-10,
    max_iter=10000,
    solver="lbfgs"
)
logistic_machine.fit(data_training, target_training)
predictions = logistic_machine.predict(data_test)

# support vector machine ------------------------------------------------------
#svm_model = SVC(kernel='rbf', C=1E1)
## change C to allow certain points inside the decision function
#svm_model.fit(data_training, target_training)
#predictions = svm_model.predict(data_test)

print(accuracy_score(target_test, predictions))

print(sum(target_test) / len(target_test))
print(sum(predictions) / len(predictions))

df_comparison = pd.DataFrame({
        'target': target_test,
        'pred': predictions,
        })
print(pd.crosstab(df_comparison['target'], df_comparison['pred']))
