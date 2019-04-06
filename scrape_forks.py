# #############################################################################
#                                                                             #
# This program extract username, star_time, ect. for later extraction of full
# Github profile data
###############################################################################

from urllib.request import Request, urlopen
import json
import pandas as pd
import datetime
import os
import time

if not os.path.exists('data'):
    os.mkdir('data')

with open('token/token') as f:
    token = f.read()
access_token = token
api = "https://api.github.com/"
repo = "996icu/996.ICU"
page_number = 0
users_processed = 0
stars_remaining = True
df = pd.DataFrame()


while page_number <= 0:
    print("Gathering Page {}".format(page_number))

    url = api + "repos/{0}/forks?page={1}&access_token={2}".format(repo, page_number, access_token)
    req = Request(url)
    response = urlopen(req)
    data = json.loads(response.read())
    # print(data[1])
    for repository in data:
        username =repository['owner']['login']
        # print(username)

        created_time = datetime.datetime.strptime(
            repository['created_at'],'%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
        created_time = created_time + datetime.timedelta(hours=-5) # EST
        created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')

        # pandas append don't have inplace
        df = df.append({
            'username': username,
            'created_time': created_time,
            },
            ignore_index=True
            )

    page_number += 1
    time.sleep(1.5)

print("Done Gathering Stargazers for {}".format(repo))

print(df)
