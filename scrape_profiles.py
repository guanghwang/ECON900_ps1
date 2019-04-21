'''
This code is modefied from
minimaxir/get-profile-data-of-repo-stargazers/blob/

This program collects information of given users
'''

import datetime
import time
from urllib.request import Request, urlopen
import json
import os
import pandas as pd

if not os.path.exists('data'):
    os.mkdir('data')

def collect_profile(users_start, users_end):
    df = pd.DataFrame()
    users_processed = users_start
    with open('token/token') as f:
        token = f.read()

    df_stargazers = pd.read_csv(
        'data/stargazers20190417_010857.csv', header=0, index_col=0
    )
    # print(df_stargazers.iloc[-1,:])
    # print(len(df_stargazers.index))
    df_stargazers_row = df_stargazers.shape[0]
    # print(df_stargazers_row)
    print("There are {} users in the stargazer file".format(df_stargazers_row))

    print(("Now Gathering Stargazers' GitHub Profiles from "
           "user {} to user {}").format(users_start, users_end))

    while users_processed < users_end:
        username = df_stargazers.iloc[users_processed, 1]
        # print(username)
        api = "https://api.github.com/"
        url = api + "users/{}?access_token={}".format(username, token)
        req = Request(url)
        response = urlopen(req)
        data = json.loads(response.read())

        time_created = datetime.datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%SZ'
        )
        time_created = time_created + datetime.timedelta(hours=-5) # EST
        time_created = time_created.strftime('%Y-%m-%d %H:%M:%S')

        time_updated = datetime.datetime.strptime(
            data['updated_at'], '%Y-%m-%dT%H:%M:%SZ'
        )
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
            }, ignore_index=True)

        if users_processed % 100 == 0:
            print("{} Users Processed: {}".format(users_processed,
                                                  datetime.datetime.now()
                                                  ))
        time.sleep(1)

        users_processed += 1

    print("Done collecting profiles for user {} to user {}".format(
        users_start, users_end))

    df.drop_duplicates(inplace=True)
    timestr = time.strftime("%Y%m%d_%H%M%S")
    filename = "profiles_u{0}u{1}_{2}.csv".format(
        users_start, users_end, timestr
    )
    print(filename)
    df.to_csv('data/'+filename)

collect_profile(0, 1)
