###############################################################################
# This code is modefied from                                                  #
# minimaxir/get-profile-data-of-repo-stargazers/blob/                         #
#                                                                             #
# This program collects information of given users                            #
###############################################################################

import pandas as pd
import datetime
import time
from urllib.request import Request, urlopen
import json
import os

if not os.path.exists('data'):
    os.mkdir('data')

df = pd.DataFrame()
users_processed = 0
with open('token/token') as f:
    token = f.read()

df_stargazers = pd.read_csv('data/stargazers_p500.csv', header=0, index_col=0)
# print(df_stargazers.iloc[-1,:])
# print(len(df_stargazers.index))
df_stargazers_row = df_stargazers.shape[0]
# print(df_stargazers_row)
print("There are {} users in the stargazer file".format(df_stargazers_row))

print("Now Gathering Stargazers' GitHub Profiles...")

while users_processed < df_stargazers_row:
    username = df_stargazers.iloc[users_processed, 1]
    # print(username)
    api = "https://api.github.com/"
    url = api + "users/{}?access_token={}".format(username, token)
    req = Request(url)
    response = urlopen(req)
    data = json.loads(response.read())

    time_created = datetime.datetime.strptime(data['created_at'],'%Y-%m-%dT%H:%M:%SZ')
    time_created = time_created + datetime.timedelta(hours=-5) # EST
    time_created = time_created.strftime('%Y-%m-%d %H:%M:%S')

    time_updated = datetime.datetime.strptime(data['updated_at'],'%Y-%m-%dT%H:%M:%SZ')
    time_updated = time_updated + datetime.timedelta(hours=-5) # EST
    time_updated = time_updated.strftime('%Y-%m-%d %H:%M:%S')

    df = df.append({
        "user_name": username,
        "user_id": data['id'],
        "bio": data['bio'],
        "num_followers": int(data['followers']),
        "num_following": int(data['following']),
        "num_repos": int(data['public_repos']),
        "location": data['location'],
        "time_created": time_created,
        "time_updated": time_updated,
        },
        ignore_index=True
        )

    users_processed += 1

    if users_processed % 100 == 0:
        print("{} Users Processed: {}".format(users_processed,
                                              datetime.datetime.now()
                                              ))
    time.sleep(1)

df.to_csv('data/profiles_0to15029.csv')

