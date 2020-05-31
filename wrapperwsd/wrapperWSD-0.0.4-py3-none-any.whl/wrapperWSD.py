#!/usr/bin/python3
# -*- coding: utf-8 -*-

#https://stackoverflow.com/questions/8077641/how-to-get-the-wordnet-synset-given-an-offset-id
#https://pythonprogramming.net/installing-nltk-nlp-python/

import pywsd
import subprocess
import urllib.parse
import xmltodict
import pickle
import os
from pathlib import Path
from nltk.corpus import wordnet

syns = list(wordnet.all_synsets())
synset2offset = dict([(s,s.offset()) for s in syns])

path = Path(__file__).parent.absolute()
wd2wiki = pickle.load(open(os.path.join(path, "resources/wd2wiki.pkl"), "rb"))
sensenindex2wd = pickle.load(open(os.path.join(path, "resources/sensenindex2wd.pkl"), "rb"))

class WrapperWSD:
    
    def __init__(self):
        self.number_of_request = 10
        self.BabelfyUrl = "https://babelfy.io/v1/disambiguate"
        self.gKey = 'KEY'
        self.value = {}
        self.value["source_NWSDT"] = "."
        pass
    
    ## =====================
    # https://github.com/alvations/pywsd
    #
    # input example: My sister has a dog. She loves him.
    # sys out: [('My', None), ('sister', Synset('sister.n.02')), 
    #    ('has', None), ('a', None), ('dog', Synset('pawl.n.01')), 
    #    ('.', None), ('She', None), ('loves', Synset('sleep_together.v.01')),
    #    ('him', None), ('.', None)]
    #
    # output: We return only those words with a SynsetID, and we include the start/end position
    #   [('sister', Synset('sister.n.02'), 3, 9), ('dog', Synset('pawl.n.01'), 16, 19), 
    #    ('loves', Synset('sleep_together.v.01'), 25, 30)]
    #
    # ------------
    # Requirements
    # ------------
    # pip3 install -U nltk
    # >>> import nltk
    # >>> nltk.download('wordnet')
    # python3 -m nltk.downloader 'popular'
    # pip3 install -U pywsd
    #
    #  input example:
    #  -------------
    #     wsd = WrapperWSD()
    #     wsd.wsdNLTK(u'My sister has a dog. She loves him.')
    #
    #  output example:
    #  --------------
    #    [('sister', Synset('sister.n.02'), 3, 9), ('dog', Synset('pawl.n.01'), 16, 19),
    #     ('loves', Synset('sleep_together.v.01'), 25, 30)]

    def wsdNLTK(self, text):
        L = pywsd.disambiguate(text)
        L_ = []
        
        txt = text
        overall = 0
        for l in L:
            if l[1]:
                p = txt.find(l[0])
                if p != -1:
                    L_.append(tuple([l[0],l[1],overall + p, overall + p + len(l[0])]))
                    overall = overall + p
                    txt = text[overall:]
                else:
                    L_.append(tuple([l[0],l[1],None,None]))
        return L_
    
    
    
    # the same as wsdNLTK, but returning the offset instead the synset_id
    #
    #  input: Barack Obama was the president of the USA. He was the best of them.
    #  output: [('president', 597265, 21, 30), ('USA', 8394922, 38, 41), ('best', 67379, 54, 58)]
    def wsdNLTK_offset(self, txt):
        L = self.wsdNLTK(txt)
        l = L[0]
        return [(x[0], synset2offset[x[1]], x[2], x[3]) for x in L]
    
    
    
    # Here I use the mapping
    #
    #    https://www.informatik.tu-darmstadt.de/media/ukp/data/fileupload_2/lexical_resources/MillerGurevych2014_alignment.tar_1.zip
    #
    # Between Wikipedia and WordNet in order to replace the sense by its corresponding Wikipedia page.
    # It was proposd in the paper:
    #
    #    []  Tristan Miller and Iryna Gurevych. WordNet-Wikipedia-Wiktionary: Construction of a Three-way Alignment.
    #         In Proceedings of the 9th International Conference on Language Resources and Evaluations (LREC 2014), May 2014.
    # With this corpus I created the dictionary wd2wiki
    # 
    # Input:  Barack Obama was the president of the USA. He was the best of them.
    # Output: [{'start': 38, 'end': 41, 'label': 'USA', 'link': 'United_States_Army'}]
    #
    def wsdNLTK_links(self, txt):
        L = self.wsdNLTK_offset(txt)
        return [{'start': x[2], 'end': x[3], 'label': x[0], 'link': wd2wiki[x[1]]} for x in L if x[1] in wd2wiki]
    
    
    # It gives only sinsets, e.g.,
    #  > [('My', None), ('sister', Synset('sister.n.02')), ('has', None), ('a', None), 
    #     ('dog', Synset('pawl.n.01')), ('.', None), ('She', None), ('loves', Synset('sleep_together.v.01')),
    #     ('him', None), ('.', None)]
    def wsdNLTK_disambiguate(self, text):
        return pywsd.disambiguate(text)
    
    
    # It gives only the sinset for an specific word in a sentence, e.g., 
    #  > Synset('sister.n.03')
    def wsdNLTK_word2sinset(self, sent, word):
        return pywsd.lesk.simple_lesk(sent,word)
    
    # It gives only the definition for an specific word in a sentence, e.g., output for "sister",
    #  > a female person who is a fellow member of a sorority or labor union or other group
    def wsdNLTK_word2definition(self, sent, word):
        answer =  pywsd.lesk.simple_lesk(sent,word)
        return answer.definition()
    
    
    
    ## =============
    # Babelfy
    # https://babelnet.org/guide
    #
    # Requirements
    # ------------
    # pip3 install xmltodict
    #
    def babelfy_request_curl(self,text,key):
        query_post = "lang=EN&key="+key+"&annType=ALL&text="+urllib.parse.quote(text)
        for i in range(self.number_of_request):
            try:
                p = subprocess.Popen(['curl', '--data', query_post, self.BabelfyUrl],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                if stdout:
                    self.raw_output = stdout
                    return stdout
            except Exception as err:
                print(err)
                continue
        return None
    
    ##
    # input: My sister has a dog. She loves him.
    # output: [('sister', 'bn:00071838n', 3, 9), ('dog', 'bn:00015267n', 16, 19), ('loves', 'bn:00090504v', 25, 30)]
    #
    # We return only those words with a babelSynsetID
    def wsdBabelfy(self,text,key=None):
        if key == None:
            key = self.gKey
        req = self.babelfy_request_curl(text,key)
        list_response = eval(req)

        R = []
        for entity in list_response:
            ini = None
            fin = None
            sinset = None
            try:
                ini = entity["charFragment"]["start"]
                fin = entity["charFragment"]["end"]+1
                sinset = entity["babelSynsetID"]
                label = text[ini:fin]
            except:
                continue
            R.append(tuple([label,sinset,ini,fin]))
        return R
    
    
    
    ##==============
    # repo: https://github.com/getalp/disambiguate
    # Note: Here, I will return only those disambiguations who has a sense in the senseindex2wd dicionary, and also, in wd2wiki
    
    
    #
    def find_word_backward(self, text, pos):
        p = pos 
        while(p>=0 and not text[p] in ['\t', '\n', ' ']):
            p = p - 1

        return [p+1, text[p+1: pos]]
    
    

    #
    def find_word_forward(self, text, pos):
        p = pos 
        while(p<=len(text) and not text[p] in ['\t', '\n', ' ']):
            p = p+1

        return [p, text[pos: p]]


    # input: 'My sister|sister%1:18:00:: has|have%2:40:00:: a dog. She loves|love%2:37:00:: him.'
    # output [{'label': 'sister', 'start': 3, 'end': 9, 'link': 'https://en.wikipedia.org/wiki/Sibling'}]
    def NWSDT_process_output(self, bout, text_):
        '''
        input: b'My sister|sister%1:18:00:: has|have%2:40:00:: a dog. She loves|love%2:37:00:: him.'
        '''
        resp = []
        
        import pickle
        pickle.dump(bout, open("bout.pkl", "wb"))
        
        
        out_full = str(bout, 'utf-8')
        out = out_full
        overall = 0
        overall_marked = 0
        while True:
            
            p_ini = out.find("|")
            
            [psense, sense] = self.find_word_forward(out, p_ini+1)
            
            if p_ini == -1:
                return resp
            else:
                overall = overall + p_ini + 1
                overall_marked = overall_marked + p_ini +1
                out = out_full[overall_marked:]
            [plabel, label] = self.find_word_backward(out_full, overall_marked-1)
            
            overall_marked = overall_marked + len(sense) + 1

            while overall_marked+1<len(out_full) and overall+1 < len(text_) and out_full[overall_marked] != text_[overall]:
                overall = overall + 1
                
            end = overall -1
            start = overall - len(label) -1
            
            if sense in sensenindex2wd:
                wd = sensenindex2wd[sense]
                if wd in wd2wiki:
                    wiki = wd2wiki[wd]
                    resp.append({
                        "label": label,
                        "start": start,
                        "end": end,
                        "link": wiki
                    })
                    
            out = out_full[overall_marked:]
        return resp

    

            
    
    #  input: {1:"sentence text 1", ...}
    #  output:{1:[{'start': 38, 'end': 41, 'label': 'USA', 'link': 'United_States_Army'}] , ... }
    
    def wsdNWSDT_links(self, text, repo_source_code=None):
        import time
        
        if not repo_source_code:
            repo_source_code = self.value["source_NWSDT"]
        elif repo_source_code[-1] == "/":
            repo_source_code = repo_source_code[:-1]
            
        
        DATADIR = repo_source_code + "/data"
        command = repo_source_code+f"/decode.sh --data_path {DATADIR}/ --weights {DATADIR}/model_weights_wsd*"
       
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        print("delay ... ")
        time.sleep(15)
        print("... expired delay")
        output = {}

        text_bytes = bytes(text.replace("\n"," ") + "\n", 'utf-8')
        process.stdin.write(text_bytes)
        process.stdin.flush()
        out = process.stdout.readline()
        pickle.dump(out, open("bout1.pkl","wb"))

        process.stdin.close()
        process.terminate()
        process.wait(timeout=0.2)
        return self.NWSDT_process_output(out, text)
