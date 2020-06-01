import requests, webbrowser
from bs4 import BeautifulSoup

def dl():
	res = requests.get(f"https://m.apkpure.com/search?q={app_name}")
	soup = BeautifulSoup(res.text, 'html.parser')
	result = soup.select('.dd')
	for link in result[:1]:
		res2 = requests.get("https://m.apkpure.com" + link.get('href') + "/download?from=details")
		soup2 = BeautifulSoup(res2.text, 'html.parser')
		result = soup2.select('.ga')
		for link in result:
			print(link.get('href'))
if __name__ == "__main__":
	app_name = "cpu"
	dl()