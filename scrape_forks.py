'''
This program collect username, created time, updated time and pushed time of
forks.
'''

import datetime
import os
import time
import json
from urllib.request import Request, urlopen
import pandas as pd

if not os.path.exists('data'):
    os.mkdir('data')

with open('token/token') as f:
    access_token = f.read()

api = "https://api.github.com/"
repo = "996icu/996.ICU"
page_number = 0
page_remaining = True
df = pd.DataFrame()

print("Staring Gathering forks")

while page_remaining:
    url = api + "repos/{0}/forks?page={1}&access_token={2}".format(
        repo, page_number, access_token
        )
    req = Request(url)
    response = urlopen(req)
    data = json.loads(response.read())
    # print(data[1])
    for repository in data:
        username = repository['owner']['login']
        # print(username)

        created_time = datetime.datetime.strptime(
            repository['created_at'], '%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
        created_time = created_time + datetime.timedelta(hours=-5) # EST
        created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')

        updated_time = datetime.datetime.strptime(
            repository['updated_at'], '%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
        updated_time = updated_time + datetime.timedelta(hours=-5) # EST
        updated_time = updated_time.strftime('%Y-%m-%d %H:%M:%S')

        pushed_time = datetime.datetime.strptime(
            repository['pushed_at'], '%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
        pushed_time = pushed_time + datetime.timedelta(hours=-5) # EST
        pushed_time = pushed_time.strftime('%Y-%m-%d %H:%M:%S')

        # pandas append don't have inplace
        df = df.append({
            'username': username,
            'created_time': created_time,
            'updated_time': updated_time,
            'pushed_time': pushed_time,
            }, ignore_index=True)

    # print(len(data))
    if len(data) < 30:
        page_remaining = False
        print("The total page is {}".format(page_number))
    time.sleep(1)

    if page_number % 100 == 0:
        print('{0} Pages Processed: {1}'.format(page_number,
                                                datetime.datetime.now()))

    page_number += 1

print("Done Gathering Forks for {}".format(repo))

df.drop_duplicates(inplace=True)

timestr = time.strftime("%Y%m%d_%H")

df.to_csv('data/forks' + timestr + '.csv')
