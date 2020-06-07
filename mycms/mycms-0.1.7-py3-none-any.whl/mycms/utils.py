
import requests
from bs4 import BeautifulSoup


url = "https://www.iconfinder.com/iconsets/tango-icon-library"


r = requests.get(url)
html = r.text

soup = BeautifulSoup(html)
icon_previews = soup.findAll("div", {"class":"icon-preview"})

for icon_preview in icon_previews:
    print("wget {}".format(icon_preview["data-preview-url"]))


    
    
    
    
    
    
    
    
