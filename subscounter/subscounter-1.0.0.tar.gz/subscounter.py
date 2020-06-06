import urllib.request
import json
import time


anahtar = "AIzaSyCsWZBH9N5wTMmjwk6uUH4LBUKP1MJZpaU"


def subs(chnl, api):
    ad= chnl
    veri = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+ad+"&key="+api).read()
    aboneler = json.loads(veri)["items"][0]["statistics"]["subscriberCount"]
    p = "{:,d}".format(int(aboneler))
    p = p.replace(',', '')
    p = int(p)
    print("The ",chnl," channel has ",p," subscribers.")