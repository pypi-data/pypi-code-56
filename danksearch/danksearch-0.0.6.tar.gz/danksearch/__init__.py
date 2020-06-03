#! /usr/bin/python3
import aiohttp, bs4, asyncio, discord
from io import BytesIO
from PIL import Image
import os, pkgutil
sfilter=pkgutil.get_data(__package__, 'safesearchfilter.txt').decode('utf-8').replace("\r","").split("\n")
#print(sfilter)
SAFESEARCH=False
class ImageDataNotFound(Exception):
    '''No data about the thumbnail could be found because the video wasn't searched yet'''
    pass
class BadRequest(Exception):
    '''Non 200 response code'''
    pass
class Video:
    def __init__(self,advanced=False):
        if SAFESEARCH:
            self.__censoredcontent=sfilter
        self.url=None
        self.advanced=advanced
        self.title=None
        self.thumbnail=None
        if self.advanced:
            self.views=None
            self.published_on=None
            self.channel=None
            self.creator=None
            self.likes=None
            self.dislikes=None
            self.description=None
    async def search(self, name, index=0, retries=5):
        if SAFESEARCH:
            for word in self.__censoredcontent:
                name=name.lower().replace(word,"")
        if retries==0:
            print("Exceeded max retry limit")
            return
        if name=="":
            name="never gonna give you up"
        # Create a url and send a request to youtube about it
        queryurl = ('http://www.youtube.com/results?search_query=' + name)
        async with aiohttp.ClientSession() as session:
            async with session.get(queryurl) as r:
                if r.status == 200:
                    text=await r.text()
                else:
                    raise BadRequest
        # Parse data using bs4
        soup = bs4.BeautifulSoup(text, 'html.parser')
        contents=[ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
        if not contents:
            print(f"Couldn't fetch video, retrying...")
            await self.search(name,index,retries=retries-1)
        try:
            self.url='http://www.youtube.com'+contents[index].a["href"]
            self.thumbnail=contents[index].img["src"]
            self.title=contents[index].h3.a["title"]
            if self.advanced:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.url) as r:
                        if r.status == 200:
                            text=await r.text()
                        else:
                            raise BadRequest     
                soup = bs4.BeautifulSoup(text, 'html.parser')
                self.views=soup.select_one(".watch-view-count").text.strip()
                self.published_on=soup.select_one(".watch-time-text").text.strip()
                __creatorinfo=soup.select_one(".yt-user-info")
                self.channel="https://youtube.com"+__creatorinfo.a["href"]
                self.creator=__creatorinfo.a.text.strip()
                __likebtn=soup.select_one('.like-button-renderer')
                self.likes=__likebtn.select_one(".like-button-renderer-like-button").text.strip()
                self.dislikes=__likebtn.select_one(".like-button-renderer-dislike-button").text.strip()
                self.description=soup.select_one("#watch-description-text").text
        except Exception as ex:
            print(f"Error: {ex}, retrying...")
            await self.search(name,index,retries=retries-1)
    async def image(self):
        if not self.thumbnail:
            raise ImageDataNotFound
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.thumbnail) as r:
                    if r.status == 200:
                        resp=await r.read()
                        thumbnail=Image.open(BytesIO(resp))
                    else:
                        raise BadRequest            
            buffer = BytesIO()  # Create a Byte Buffer
            thumbnail.save(buffer,format="PNG")  # Save image to buffer in order to avoid saving to disk
            buffer.seek(0)
            return discord.File(buffer,'thumbnail.png')  # Instantiate a file object using created buffer
