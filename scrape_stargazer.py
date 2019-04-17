'''
This code is modefied from
minimaxir/get-profile-data-of-repo-stargazers/blob/

This program extract username, star_time, ect. for later extraction of full
Github profile data

The maximum amount of pages that github allow to scrape is 1333
'''
import datetime
import os
import time
import re
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
users_processed = 0
stars_remaining = True
df = pd.DataFrame()

# determine the total number of pages of stargazers that github allows
lasturl = api + "repos/{0}/stargazers?rel=last&access_token={1}".format(
    repo, access_token
    )

lasthead = urlopen(Request(lasturl)).info().items()

maxpage_raw = re.findall(r'page=[0-9]{3,}',
                         [x for x in lasthead if x[0] == 'Link'][0][1])[0]
maxpage = int(re.findall(r'[0-9]+', maxpage_raw)[0]) - 1

print("The maximum page that Github allows is {}".format(maxpage))

# scrape data -----------------------------------------------------------------
print("Gathering Stargazers for {}...".format(repo))

while page_number <= maxpage:
    # print("Gathering Page {}".format(page_number))
    url = api + "repos/{0}/stargazers?page={1}&access_token={2}".format(
        repo, page_number, access_token
    )
    req = Request(url)
    req.add_header('Accept', 'application/vnd.github.v3.star+json')
    response = urlopen(req)
    data = json.loads(response.read())
    # print(data[1])
    for user in data:
        username = user['user']['login']
        # print(username)

        star_time = datetime.datetime.strptime(
            user['starred_at'], '%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
        star_time = star_time + datetime.timedelta(hours=-5) # EST
        star_time = star_time.strftime('%Y-%m-%d %H:%M:%S')

        # pandas append don't have inplace
        df = df.append({
            'username': username,
            'star_time': star_time,
            }, ignore_index=True)

    if page_number % 100 == 0:
        print('{0} Pages Processed: {1}'.format(page_number,
                                                datetime.datetime.now()))

    page_number += 1
    time.sleep(1)

print("Done Gathering Stargazers for {}".format(repo))

df.drop_duplicates(inplace=True)

timestr = time.strftime("%Y%m%d_%H%M%S")

df.to_csv('data/stargazers' + timestr + '.csv')
