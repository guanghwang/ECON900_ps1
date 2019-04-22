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
    url = api + "repos/{0}/issues?page={1}&state=all&access_token={2}".format(
        repo, page_number, access_token
    )
    req = Request(url)
    response = urlopen(req)
    data = json.loads(response.read())
    for issue in data:
        issue_id = issue['id']
        title = issue['title']
        username = issue['user']['login']
        # print(username)

        created_time = datetime.datetime.strptime(
            issue['created_at'], '%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
        created_time = created_time + datetime.timedelta(hours=-5) # EST
        created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')

        updated_time = datetime.datetime.strptime(
            issue['updated_at'], '%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
        updated_time = updated_time + datetime.timedelta(hours=-5) # EST
        updated_time = updated_time.strftime('%Y-%m-%d %H:%M:%S')
        
        if issue['closed_at'] == None:
            closed_time = ''
        else:
            closed_time = datetime.datetime.strptime(
                issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ'
            ) # Zulu time(UTC)
            closed_time = closed_time + datetime.timedelta(hours=-5) # EST
            closed_time = closed_time.strftime('%Y-%m-%d %H:%M:%S')

        if issue['pull_request'] != None:
            pull_request = 1
            pull_url = issue['pull_request']['url']
        else:
            pull_request = 0
            pull_url = ""

        # pandas append don't have inplace
        df = df.append({
            'issue_id': issue_id,
            'title': title,
            'body': issue['body'],
            'username': username,
            'state': issue['state'],
            'created_time': created_time,
            'updated_time': updated_time,
            'closed_time': closed_time,
            'pull_request': pull_request,
            'pull_url': pull_url,
            }, ignore_index=True)
    
    if page_number == 0:
        page_len = len(data)

    # print(len(data))
    if len(data) < page_len:
        page_remaining = False
        print("The total page is {}".format(page_number))
    time.sleep(1)

    if page_number % 10 == 0:
        print("{} Pages Processed: {}".format(
            page_number,
            datetime.datetime.now()
        ))

    page_number += 1

print("Done Gathering issues for {}".format(repo))
# print(df)
# print(df.iloc[0,])

df.drop_duplicates(inplace=True)
timestr = time.strftime("%Y%m%d_%H%M%S")
df.to_csv('data/issues' + timestr + '.csv')
