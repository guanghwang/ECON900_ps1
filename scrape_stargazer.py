# #############################################################################
# This code is modefied from
# minimaxir/get-profile-data-of-repo-stargazers/blob/
#
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
repo = "996icu/996.ICU"
page_number = 0
users_processed = 0
stars_remaining = True
df = pd.DataFrame()

# # test one page
# url = "https://api.github.com/repos"
# url = url + "/{0}/stargazers?page={1}&access_token={2}".format(repo, page_number, access_token)
# req = Request(url)
# req.add_header('Accept', 'application/vnd.github.v3.star+json')
# response = urlopen(req)
# data = json.loads(response.read())
# print(data[1])

print("Gathering Stargazers for {}...".format(repo))

while page_number <= 500:
    print("Gathering Page {}".format(page_number))

    url = "https://api.github.com/repos"
    url = url + "/{0}/stargazers?page={1}&access_token={2}".format(repo, page_number, access_token)
    req = Request(url)
    req.add_header('Accept', 'application/vnd.github.v3.star+json')
    response = urlopen(req)
    data = json.loads(response.read())
    # print(data[1])
    for user in data:
        username = user['user']['login']
        # print(username)

        star_time = datetime.datetime.strptime(
            user['starred_at'],'%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
        star_time = star_time + datetime.timedelta(hours=-5) # EST
        star_time = star_time.strftime('%Y-%m-%d %H:%M:%S')

        # pandas append don't have inplace
        df = df.append({
            'username': username,
            'star_time': star_time,
            },
            ignore_index=True
            )

    page_number += 1
    time.sleep(1.5)

print("Done Gathering Stargazers for {}".format(repo))

df = df.drop_duplicates()

df.to_csv('data/stargazers_p500.csv')
