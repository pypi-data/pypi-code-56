import tweepy
import time
import json

from io import BytesIO
import os
from urllib.parse import urlparse

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class API(object):
    def __load_tweet_dict(self, tweet_id_str):
        return json.loads(json.dumps(self._twitter.get_status(tweet_id_str)._json))

    @staticmethod
    def __is_retweet(tweet_dict):
        return 'retweeted_status' in tweet_dict

    @staticmethod
    def __is_reply(tweet_dict):
        return not tweet_dict['in_reply_to_status_id'] is None

    @staticmethod
    def __is_quote(tweet_dict):
        return tweet_dict['is_quote_status']

    def __build_thread(self, tweet_dict):
        tweet_dict_list = []
        tweet_dict_list.insert(0, tweet_dict)

        if not self.__is_reply(tweet_dict):
            return tweet_dict_list

        replied_tweet_dict = self.__load_tweet_dict(tweet_dict['in_reply_to_status_id_str'])

        while self.__is_reply(replied_tweet_dict):
            replied_tweet_dict = self.__load_tweet_dict(replied_tweet_dict['in_reply_to_status_id_str'])
            tweet_dict_list.insert(0, replied_tweet_dict)

        #        while self.__is_reply(replied_tweet_dict) and replied_tweet_dict['in_reply_to_user_id'] == \
        #               replied_tweet_dict['user']['id']:
        #          replied_tweet_dict = self.__load_tweet_dict(replied_tweet_dict['in_reply_to_status_id_str'])
        #          tweet_dict_list.insert(0, replied_tweet_dict)

        return tweet_dict_list

    @staticmethod
    def __take_all_articles_screenshots(tweet_url):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1920, 4320)

        # preload cookies
        driver.get(tweet_url)

        # consent the bloody cookies...
        driver.add_cookie({"name": "eu_cn", "value": "1"})

        # we will have to wait for frontend app to render everything
        wait = WebDriverWait(driver, 10)

        driver.get(tweet_url)

        elements = wait.until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'article'))
        )

        driver.execute_script('window.scrollTo(0, 0)')
        time.sleep(5)

        driver.save_screenshot(os.path.basename(urlparse(tweet_url).path) + '.debug.png')

        screenshots = []

        for element in elements:
            # actions.move_to_element(element).perform()
            # png = element.screenshot_as_png(str(i) + image_path)
            screenshots.append(
                Image.open(BytesIO(element.screenshot_as_png))
            )
        driver.quit()
        return screenshots

    def __init__(self,
                 twitter_consumer_key,
                 twitter_secret,
                 twitter_access_token,
                 twitter_access_token_secret):
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_secret)
        auth.set_access_token(twitter_access_token, twitter_access_token_secret)
        self._twitter = tweepy.API(auth)

    def take_tweet_screenshot(self, tweet_id, path):
        tweet_dict = self.__load_tweet_dict(str(tweet_id))
        tweet_dict_list = self.__build_thread(tweet_dict)

        index_in_thread = 0
        for item in tweet_dict_list:
            if item['id'] == tweet_id:
                break
            index_in_thread = index_in_thread + 1

        tweet_url = 'https://twitter.com/{}/status/{}'.format(
            tweet_dict['user']['screen_name'],
            tweet_dict['id_str'])
        screenshots = self.__take_all_articles_screenshots(tweet_url)

        thread_height = 0
        for i in range(index_in_thread + 1):
            thread_height = thread_height + screenshots[i].height

        img = Image.new('RGB', (screenshots[0].width, thread_height))

        cursor = 0
        for i in range(index_in_thread + 1):
            img.paste(screenshots[i], (0, cursor))
            cursor = cursor + screenshots[i].height

        img.save(path)

    def take_twitter_thread_screenshot(self, tweet_id, path):

        return
