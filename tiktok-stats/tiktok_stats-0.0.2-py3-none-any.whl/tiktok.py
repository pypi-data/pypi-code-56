import json
from typing import Generator

from tiktok_stats.scrapers.scraper import Scraper


class TikTokScraper(Scraper):
    USER_URL = 'https://www.tiktok.com/@'
    API_URL = 'https://www.tiktok.com/api/item_list/?count=15&id={id}&type=1&maxCursor=0&minCursor=0&sourceType=8&appId=1233&region=PL&language=pl'
    
    def get_user_data(self, username: str):
        """ Fetches raw user account and posts data.
        """
        print(self.USER_URL + username)
        soup = self.make_request(self.USER_URL + username)
        data = self._extract_json_from_source(soup)
        data = data['props']['pageProps']
        user_stats = data['userInfo']['stats']
        user_info = data['userInfo']['user']

        avatar_medium = user_info['avatarMedium']
        avatar_thumb = user_info['avatarThumb']
        nickname = user_info['nickname']
        signature = user_info['signature']
        verified = user_info['verified']
        user_id = user_info['id']
        sec_uid = user_info['secUid']

        followers = user_stats['followerCount']
        following = user_stats['followingCount']
        likes = user_stats['heartCount']
        videos = user_stats['videoCount']

        api_url = self.API_URL.format(id=user_id)
        print(api_url)
        posts = list(self.parse_posts(api_url))

        return {
            'username': username,
            'followers': followers,
            'following': following,
            'likes': likes,
            'videos': videos,
            'tiktok_account_data': {
                'avatar_medium': avatar_medium,
                'avatar_thumb': avatar_thumb,
                'nickname': nickname,
                'signature': signature,
                'verified': verified,
                'id': user_id,
                'sec_uid': sec_uid
            },
            'posts': posts
        }

    def parse_posts(self, url) -> Generator[dict, None, None]:
        data = self.make_request(url, json_=True)
        for item in data['items']:
            tags = [x['hashtagName'] for x in item['textExtra'] if x.get('hashtagName')] \
                if item.get('textExtra') else []
            yield {
                'create_time': item['createTime'],
                'desc': item['desc'],
                'music': item.get('music'),
                'stats': item['stats'],
                'tags': tags
            }

    @staticmethod
    def _extract_json_from_source(soup):
        script = str(soup.find('script', {'id': '__NEXT_DATA__'}))
        script = script.replace('<script crossorigin="anonymous" id="__NEXT_DATA__" type="application/json">', ''). \
            replace('</script>', '')
        return json.loads(script)
