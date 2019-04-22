'''
This program extract username, star_time, ect. for later extraction of full
Github profile data
'''

from urllib.request import Request, urlopen
import json
import datetime
import os
import time
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


print("Staring Gathering pulls")

while page_remaining:
    url = api + "repos/{0}/pulls?page={1}?state=all&access_token={2}".format(
        repo, page_number, access_token
    )
    req = Request(url)
    response = urlopen(req)
    data = json.loads(response.read())
    for pull in data:
        pull_id = pull['id']
        title = pull['title']
        username = pull['user']['login']
        # print(username)

        created_time = datetime.datetime.strptime(
            pull['created_at'], '%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
        created_time = created_time + datetime.timedelta(hours=-5) # EST
        created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')

        updated_time = datetime.datetime.strptime(
            pull['updated_at'], '%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
        updated_time = updated_time + datetime.timedelta(hours=-5) # EST
        updated_time = updated_time.strftime('%Y-%m-%d %H:%M:%S')

        if pull['merged_at'] == "":
            merged_time = datetime.datetime.strptime(
                pull['merged_at'], '%Y-%m-%dT%H:%M:%SZ'
                ) # Zulu time(UTC)
            merged_time = closed_time + datetime.timedelta(hours=-5) # EST
            merged_time = closed_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            merged_time = ""

        if pull['state'] == 'closed':
            closed_time = datetime.datetime.strptime(
                pull['closed_at'], '%Y-%m-%dT%H:%M:%SZ'
                ) # Zulu time(UTC)
            closed_time = closed_time + datetime.timedelta(hours=-5) # EST
            closed_time = closed_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            closed_time = ""

        # pandas append don't have inplace
        df = df.append({
            'pull_id': pull_id,
            'title': title,
            'body': pull['body'],
            'username': username,
            'state': pull['state'],
            'created_time': created_time,
            'updated_time': updated_time,
            'closed_time': closed_time,
            'merged_time': merged_time,
            }, ignore_index=True)

    # print(len(data))
    if len(data) < 3:
        page_remaining = False
        print("The total page is {}".format(page_number))
    time.sleep(1)

    if page_number % 10 == 0:
        print("{} Pages Processed: {}".format(
            page_number,
            datetime.datetime.now()
        ))

    page_number += 1

print("Done Gathering pulls for {}".format(repo))
# print(df)
# print(df.iloc[0,])

df.drop_duplicates(inplace=True)
timestr = time.strftime("%Y%m%d_%H%M%S")
df.to_csv('data/pulls' + timestr + '.csv')
