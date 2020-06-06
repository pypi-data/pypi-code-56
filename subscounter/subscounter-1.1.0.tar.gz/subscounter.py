import urllib.request
import json
import time




def subs_counter_by_channel_name(chnl, api):
    ad= chnl
    veri = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+ad+"&key="+api).read()
    aboneler = json.loads(veri)["items"][0]["statistics"]["subscriberCount"]
    p = "{:,d}".format(int(aboneler))
    p = p.replace(',', '')
    p = int(p)
    print("The ",chnl," channel has ",p," subscribers.")
def subs_counter_by_channel_id(chnl, api):
    ad= chnl
    veri = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id="+ad+"&fields=items/statistics/subscriberCount&key="+api).read()
    aboneler = json.loads(veri)["items"][0]["statistics"]["subscriberCount"]
    p = "{:,d}".format(int(aboneler))
    p = p.replace(',', '')
    p = int(p)
    print("The ",chnl," channel has ",p," subscribers.")