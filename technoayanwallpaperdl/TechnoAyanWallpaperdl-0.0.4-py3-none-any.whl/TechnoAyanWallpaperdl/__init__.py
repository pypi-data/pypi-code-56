from googlesearch import search
from bs4 import BeautifulSoup as bs
import requests

def dl(srch):
	query = srch+" wallpapers cave"
	
	for p_link in search(query, tld="co.in", num=1, stop=1, pause=1):
		page = p_link
		
		r = requests.get(f"{page}")
		
		s = bs(r.text, 'html.parser')
		
		dl_links = s.select('.download')
	
	for link in dl_links[0:1]:
		image_url = link.get('href')
		r1 = "https://wallpapercave.com"+image_url
		
	for link in dl_links[1:2]:
		image_url = link.get('href')
		r2 = "https://wallpapercave.com"+image_url
		
	for link in dl_links[2:3]:
		image_url = link.get('href')
		r3 = "https://wallpapercave.com"+image_url
		
	for link in dl_links[3:4]:
		image_url = link.get('href')
		r4 = "https://wallpapercave.com"+image_url
		
		d1 = requests.get(f"{r1}")
		
		with open(f"{query} 1.jpg",'wb') as f:
			f.write(d1.content)
			
		d2 = requests.get(f"{r2}")
		
		with open(f"{query} 2.jpg",'wb') as f:
			f.write(d2.content)
			
		d3 = requests.get(f"{r3}")
		
		with open(f"{query} 3.jpg",'wb') as f:
			f.write(d3.content)