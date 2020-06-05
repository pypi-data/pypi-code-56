from io import BytesIO

from PIL import Image
from bs4 import BeautifulSoup
from requests import Session

from ._utils import try_get_vcode


class RSBBSSession(Session):
    HOST = 'rsbbs.xidian.edu.cn'

    def __init__(self):
        super().__init__()

    def login(self, username, password):
        vcode = ''
        while len(vcode) != 4:
            login = self.get(f'http://{self.HOST}/member.php', params={
                'mod': 'logging',
                'action': 'login',
                'mobile': '2'
            })
            soup = BeautifulSoup(login.text, 'lxml')
            img = soup.find('img', {'class': 'seccodeimg'}).get('src')
            vcode = try_get_vcode(Image.open(
                BytesIO(self.get(f'http://{self.HOST}/{img}', headers={
                    'Referer': login.url
                }).content)
            ))
        page = self.post(
            f'http://{self.HOST}/' +
            soup.find('form', id='loginform').get('action')
        ).text
        if '欢迎您回来' not in page:
            print(page)
            return self.login(username, password)
        return
