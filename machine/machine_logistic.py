'''
logistic machine
'''
#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

df = pd.read_csv(
    './../data/tidy_data.csv',
    index_col=0,
    header=0
)

# drop nas
df = df[pd.notnull(df['time_created'])]
data_name = ['num_followers',
             'num_following',
             'num_repos',
             'days_created',
             'days_updated'
             ]
data = df.loc[:, data_name]
data['days_created_pos'] = (data['days_created'] > 0) * 1
data['num_followers_pos'] = (data['num_followers'] > 0) * 1
data['num_followers2'] = np.square(data['num_followers'])
data['num_following_pos'] = (data['num_following'] > 0) * 1
data['num_following2'] = np.square(data['num_following'])
data['num_repos_pos'] = (data['num_repos'] > 0) * 1
data['num_repos2'] = np.square(data['num_repos'])
target = df.loc[:, 'pull_request'].values

# summary statistics ----------------------------------------------------------
print(df.loc[df['pull_request'] == 1, :].mean())
print(df.loc[df['pull_request'] == 0, :].mean())

print(len(df.loc[df['pull_request'] == 1, :]))
print(len(df.loc[df['pull_request'] == 0, :]))

# machine ---------------------------------------------------------------------
data_training, data_test, target_training, target_test = \
        train_test_split(data, target, test_size=0.80, random_state=23042019)

logistic_machine = LogisticRegression(
    random_state=23042019,
    C=1.0,
    tol=1e-10,
    max_iter=10000,
    solver="lbfgs"
)
logistic_machine.fit(data_training, target_training)
predictions = logistic_machine.predict(data_test)

print(accuracy_score(target_test, predictions))

cnf_matrix = pd.DataFrame(
    confusion_matrix(target_test, predictions),
    columns = ['Predict 0', 'Predict 1'],
    index = ['True 0', 'True 1']
)
print(cnf_matrix)

# kfolder ---------------------------------------------------------------------
kfold_machine = KFold(n_splits=5)
kfold_machine.get_n_splits(data)
kfold_accuracy = pd.DataFrame()
for training_index, test_index in kfold_machine.split(data):
    # print(len(training_index))
    # print("Training index is {}".format(training_index))
    # print("Test index is {}".format(test_index))
    # print(data.shape)
    data_training, data_test = \
        data.iloc[training_index, :], data.iloc[test_index, :]
    # print(data_training.shape)
    # print(data_test.shape)
    target_training, target_test = target[training_index], target[test_index]
    logistic_machine = LogisticRegression(
        random_state=23042019,
        C=1.0,
        tol=1e-10,
        max_iter=10000,
        solver="lbfgs"
    )
    logistic_machine.fit(data_training, target_training)
    predictions = logistic_machine.predict(data_test)
    score = accuracy_score(target_test, predictions)
    kfold_accuracy = kfold_accuracy.append({'score': score}, ignore_index=True)
    cnf_matrix = pd.DataFrame(
        confusion_matrix(target_test, predictions),
        columns = ['Predict 0', 'Predict 1'],
        index = ['True 0', 'True 1']
    )
    print(cnf_matrix)
    
print(kfold_accuracy)
