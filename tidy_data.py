'''
Clean the data from scrapping

Make it ready for machine learning

Set the time when icu 996 starts as the starting date 
and transfer date to days
'''

import glob
import datetime
import numpy as np
import pandas as pd

icu996_created_time = datetime.datetime.strptime(
    '2019-03-26T07:31:14Z', '%Y-%m-%dT%H:%M:%SZ'
) # Zulu time(UTC)
icu996_created_time = icu996_created_time + datetime.timedelta(hours=-5) # EST
icu996_created_time = icu996_created_time.strftime('%Y-%m-%d %H:%M:%S')

# profiles
df_profiles = pd.DataFrame()
for profile_path in sorted(glob.glob('data/profiles_u*')):
    df_profiles = df_profiles.append(
        pd.read_csv(profile_path, index_col=0, header=0)
    )

df_profiles.drop_duplicates(inplace=True)

df_profiles['days_created'] = (pd.to_datetime(df_profiles['time_created'])
                               - np.datetime64(icu996_created_time)).dt.days

df_profiles['days_updated'] = (pd.to_datetime(df_profiles['time_updated'])
                                  - np.datetime64(icu996_created_time)).dt.days

# forks
df_forks = pd.read_csv('data/forks20190422_205609.csv', index_col=0, header=0)

df_profiles['fork'] = 0
forks_index = df_profiles['user_name'].isin(df_forks['username'].values)
df_profiles.loc[forks_index, 'fork'] = 1

# pull request
df_request = pd.read_csv('data/issues20190422_012546.csv', index_col=0, header=0)
## if one user make multiple pull request, keep the first obs
df_request_first = df_request.groupby('username').nth(0).reset_index()
df_profiles['pull_request'] = 0
request_index = df_profiles['user_name'].isin(df_request_first['username'].values)
df_profiles.loc[request_index, 'pull_request'] = 1
#df_profiles = df_profiles.merge(
#    df_request_first.loc[:, ['username', 'pull_url']],
#    how='left',
#    left_on='user_name',
#    right_on='username'
#)

# types
df_profiles['type'] = 0 # stars
type1_index = (df_profiles['fork'] == 1) & (df_profiles['pull_request'] == 0)
df_profiles.loc[type1_index, 'type'] = 1 # forks not pull request
type2_index = (df_profiles['fork'] == 1) & (df_profiles['pull_request'] == 1)
df_profiles.loc[type2_index, 'type'] = 2 # forks and pull request
type3_index = (df_profiles['fork'] == 0) & (df_profiles['pull_request'] == 1)
df_profiles.loc[type3_index, 'type'] = 3 # not forks but pull request

df_profiles.to_csv("data/tidy_data.csv")