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

repo = "996icu/996.ICU"
page_number = 0
users_processed = 0
stars_remaining = True
df = pd.DataFrame()

print("Gathering Stargazers for {}...".format(repo))
url = "https://api.github.com/repos"
url = url + "/{0}/stargazers?page={1}".format(repo, page_number)

req = Request(url)
req.add_header('Accept', 'application/vnd.github.v3.star+json')
response = urlopen(req)
data = json.loads(response.read())
# print(data[1])
for user in data:
    username = user['user']['login']
    print(username)

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
    print(df)

print(df)
