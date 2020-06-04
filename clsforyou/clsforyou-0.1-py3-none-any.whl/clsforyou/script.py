import webbrowser
import sys

#args = sys.argv
#print(args)
#browser=webbrowser.get('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s')

def search(engine,*keywords):

    #google
    if engine == "g":
        for i in range(len(keywords)):
        	url = "https://www.google.com/search?sxsrf=ACYBGNQ3H_FH0EJkcDs4UK9blS06G4dRoA%3A1576058296257&ei=uL3wXameD-HomAWwy5CgAw&q="+keywords[i]
        	webbrowser.open(url)

    #duckduckgo
    elif engine =="d":
        for i in range(len(keywords)):
        	url = "https://duckduckgo.com/?q="+keywords[i]+"&t=h_&ia=web"
        	webbrowser.open(url)

    #yahoo
    elif engine == "y":
        for i in range(len(keywords)):
        	url = "https://search.yahoo.co.jp/search?p="+keywords[i]
        	webbrowser.open(url)

    #bing
    elif engine == "b":
        for i in range(len(keywords)):
        	url = "https://www.bing.com/search?q="+keywords[i]
        	webbrowser.open(url)

    #youtube
    elif engine == "yt":
        for i in range(len(keywords)):
        	url = "https://www.youtube.com/results?search_query="+keywords[i]
        	webbrowser.open(url)

    #niconico
    elif engine == "ni":
        for i in range(len(keywords)):
        	url = "https://www.nicovideo.jp/search/"+keywords[i]
        	webbrowser.open(url)

    #twitter
    elif engine == "tw":
        for i in range(len(keywords)):
        	url = "https://twitter.com/search?q="+keywords[i]
        	browser.open(url)

    #instagram
    elif engine == "in":
        for i in range(len(keywords)):
        	url = "https://www.instagram.com/explore/tags/"+keywords[i]
        	webbrowser.open(url)

    #hidden service
    elif engine == "hd":
        for i in range(len(keywords)):
        	url = "https://duckduckgo.com/?q=site:onion.to "+keywords[i]
        	webbrowser.open(url)


