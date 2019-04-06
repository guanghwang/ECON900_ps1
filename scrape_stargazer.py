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

repo = "996icu/996.ICU"
page_number = 0
users_processed = 0
stars_remaining = True
list_stars = []

print("Gathering Stargazers for {}...".format(repo))
url = "https://api.github.com/repos/{0}/stargazers?page={1}".format(repo, page_number)

req = Request(url)
req.add_header('Accept', 'application/vnd.github.v3.star+json')
response = urlopen(req)
data = json.loads(response.read())
print(data[0])

