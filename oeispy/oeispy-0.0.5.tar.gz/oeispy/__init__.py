from urllib import request
import requests
import json
import random
import shutil
import os

def resultEois(seq):
    res=request.urlopen('https://oeis.org/search?fmt=json&q='+seq+'&start=1')
    data = json.loads(res.read().decode())
    res=data['results']
    return res

def topResult(res):
    return res[0]

def countResult(res):
    return len(res)

def getNumber(res_indexed):
    try:
        return res_indexed['number']
    except:
        return None

def getId(res_indexed):
    try:
        return res_indexed['id']
    except:
        return None

def getData(res_indexed):
    try:
        return res_indexed['data']
    except:
        return None

def getName(res_indexed):
    try:
        return res_indexed['name']
    except:
        return None

def getComment(res_indexed):
    try:
        return res_indexed['comment']
    except:
        return None

def getLink(res_indexed):
    try:
        return res_indexed['link']
    except:
        return None

def getExample(res_indexed):
    try:
        return res_indexed['example']
    except:
        return None

def getAuthor(res_indexed):
    try:
        return res_indexed['author']
    except:
        return None

def getTime(res_indexed):
    try:
        return res_indexed['time']
    except:
        return None

def getCreated(res_indexed):
    try:
        return res_indexed['created']
    except:
        return None

def getFormula(res_indexed):
    try:
        return res_indexed['formula']
    except:
        return None

def getProgram(res_indexed):
    try:
        return res_indexed['program']
    except:
        return None

def getGraph(id):
    res = requests.get('https://oeis.org/'+id+'/graph?png=1',stream=True)
    if res.status_code==200:
        with open('graph.png', 'wb') as outf:
            shutil.copyfileobj(res.raw, outf)
        del res
        return True,os.path.realpath(outf.name)
    else:
        return False

def getRandom():
    id=str(random.randint(1,300000))
    if(len(id)<6):
        id='A'+'0'*(6-len(id))+id
    res = request.urlopen('https://oeis.org/search?fmt=json&q=' + id + '&start=1')
    data = json.loads(res.read().decode())
    res = data['results']
    return res
