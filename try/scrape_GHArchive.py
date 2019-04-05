import urllib.request
# import StringIO
import wget
import gzip
import json
import sys
import os

if not os.path.exists("GHArchive"):
    os.mkdir("GHArchive")

if not os.path.exists("GHArchive/gz"):
    os.mkdir("GHArchive/gz")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'

def ReadGHArchive(date, name):
    date = str(date)
    name = str(name)
    url = ('http://data.gharchive.org/' + date + '.json.gz')
    response = urllib.request.urlopen(
        urllib.request.Request(url, headers={'User-Agent': user_agent})
        )
    json_file = gzip.decompress(response.read())
    with open('GHArchive/events_' + name, 'wb') as f:
        f.write(json_file)


    # compressedFile = StringIO.StringIO()
    # compressedFile.write(response.read())

    # Set the file's current position to the beginning
    # of the file so that gzip.GzipFile can read
    # its contents from the top.
    # compressedFile.seek(0)
    # decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')
    # print(decompressedFile)
    # with open(outFilePath, 'w') as outfile:
    #     outfile.write(decompressedFile.read())   compressedFile.write(response.read())

    # wget.download(
    #     urllib.request.Request(url, headers={'User-Agent': user_agent}),
    #     out='./GHArchive/gz/'
    #     )
    # response = urllib.request.urlopen(
    #     urllib.request.Request(url, headers={'User-Agent': user_agent})
    #     )
    # print(g_file)
    # json_file = gzip.decompress(response)
    # with open('GHArchive' + date + '.josn') as f:
    #     f.write(json.dumps(json.load(g_file), indent=4))

ReadGHArchive('2018-06-04-15', "2018060415")

def JsonPandas():
    with open("GHArchive/"+ "events_2015-01-01-15") as f:
        for line in f:
            lastjson = json.dumps(json.loads(line))
    return(lastjson)

test = JsonPandas()