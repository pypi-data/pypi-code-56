# -*- coding: utf-8 -*-
"""
Created on Mon May  6 01:20:37 2019

@author: yuanq
"""

import twitter
import json
import enum
import dateutil
import datetime
import matplotlib.pyplot as plt

import modGlobal3
import modUtils3 as util

logger = util.get_basic_logger(__name__, util.logging.DEBUG, util.logging.WARNING)

WORLD_ID = {'WORLD':1,
            'EUROPE': 24865675,
            'UNITED_STATES':23424977,
            'SINGAPORE':1062617,
            'MALAYSIA':23424901}

WORLD_ID_INV = {value:key for key, value in WORLD_ID.items()}

#==============================================================================
#+                                                                            +
#+                             Note on Twitter                                +
#+                                                                            +
#==============================================================================
#
#- Consider that a Twitter user need not be a real person; it could be an inanimate
#  object, a company, a musical group, an imaginary persona, an impersonation of 
#  someone etc.
#- Think of interest graph as a way of modeling connections between people and
#  their arbitrary interests
#- Interest graphs provide a number of possibilities in data mining realm that
#  primarily involve measuring correlations between things for the objective of 
#  making intelligent recommendations and other applications in machine learning
#- The power of Twitter lies in its ability to enable a person to create, connect 
#  with, and explore a community of interest for an arbitrary topic of interest
#- Twitter places no particular restrictions on the persona of an account and relies
#  on self-organizing behavior such as following relationships and folksonomies
#  that emerge from the use of hashtags to create a certain kind of order within
#  the system
#
#- Tweets
#  * 280 character textual content
#  * 2 pieces of metadata
#    a. entities (associated with a tweet)
#       - user mentions
#       - hashtags
#       - URLs
#       - media
#    b. places
#       - the actual location in which a tweet was authored
#       - a reference to the place described in a tweet
#
#- Timelines
#  * chronologically sorted collections of tweets
#  * 2 types
#    a. home timeline 
#       - the view that a user sees when he logs into his account and look at all
#         the tweets from users that he is following
#    b. user timeline
#       - a collection of tweets only from a certain user
#- Streams
#  * samples of public tweets flowing through Twitter in real time

@enum.unique
class ENUM_VISUALIZATION_TYPE(enum.Enum):
    BY_WORLD_ID = 1
    BY_TWEET_NAME = 2

class TwitterData():
    def __init__(self, 
                 consumer_key = None,
                 consumer_secret = None,
                 access_token = None,
                 access_secret = None):
        self.__obj_twitter_api = self.set_twitter_api(consumer_key = consumer_key,
                                                  consumer_secret = consumer_secret,
                                                  access_token = access_token,
                                                  access_secret = access_secret)
        self.__dic_trends = dict()
                        
        
    def __repr__(self):
        pass

    def __len__(self):
        pass        

    def set_twitter_api(self,
                        consumer_key = None,
                        consumer_secret = None,
                        access_token = None,
                        access_secret = None):
        if consumer_key:
            str_consumer_key = consumer_key
        else:
            str_consumer_key = modGlobal3.CONSUMER_KEY
        
        if consumer_secret:
            str_consumer_secret = consumer_secret
        else:
            str_consumer_secret = modGlobal3.CONSUMER_SECRET
            
        if access_token:
            str_access_token = access_token
        else:
            str_access_token = modGlobal3.ACCESS_TOKEN
            
        if access_secret:
            str_access_secret = access_secret
        else:
            str_access_secret = modGlobal3.ACCESS_SECRET
            
        auth = twitter.oauth.OAuth(token = str_access_token,
                                   token_secret = str_access_secret,
                                   consumer_key = str_consumer_key,
                                   consumer_secret = str_consumer_secret)    
                    
        return twitter.Twitter(auth=auth)
    
    def get_twitter_api(self):
        return self.__obj_twitter_api
    
    def add_trends(self, int_world_id):
        obj_trend = self.Trend(self.__obj_twitter_api, int_world_id)        
        self.__dic_trends[int_world_id] = obj_trend
        return obj_trend
    
    def remove_trend(self, int_world_id):
        self.__dic_trends.pop(int_world_id)
        return self.__dic_trends
    
    def get_trend_objects(self):
        return self.__dic_trends
    
    def get_trends_by_world_id(self):
        return {key:value.get_trends() 
                    for key, value in self.__dic_trends.items()}
            
    def get_trends_by_name(self):
        dic_output = dict()
        for world_id, trends in self.__dic_trends.items():
            for name, dic_info in trends.get_trends().items():
                if name in dic_output:
                    dic_output[name][world_id] = dic_info
                else:
                    dic_output[name] = {world_id:dic_info}
        return dic_output
    
    def refresh_trends(self):
        if self.__dic_trends:
            for key, value in self.__dic_trends.items():
                created_at = value.get_created_at(True)                
                if ((datetime.datetime.now().astimezone(created_at.tzinfo) - created_at) >
                    datetime.timedelta(minutes=15)):                    
                    value.set_data() 
                    logger.info('Trend refreshed for world_id {world_id}.'.format(world_id=WORLD_ID_INV[key]))
                else:
                    logger.info('Trend NOT refreshed for world_id {world_id}.'.format(world_id=WORLD_ID_INV[key]))
            
            return True                    
        else:
            logger.info('No existing Trend.')
            return False
        
    def intersect_trends(self):
        int_num_of_trends = len(self.__dic_trends)         
        dic_trends_by_name = self.get_trends_by_name()
        
        for key in list(dic_trends_by_name.keys()):        
            if len(dic_trends_by_name[key]) != int_num_of_trends:
                dic_trends_by_name.pop(key)
#            else:
#                for world_id in list(dic_trends_by_name[key].keys()):
#                    dic_trends_by_name[key][world_id] = dic_trends_by_name[key][world_id]['tweet_volume']                    
        
        return dic_trends_by_name
    
#    def intersect_trends_old(self):    
#        
#        lst_names = []
#        for key, value in self.__dic_trends.items():            
#            lst_names.append(set(value.get_trends().keys()))
#            
#        set_intersected_names = set.intersection(*lst_names)
#        
#        self.__lst_by_name = []
#        for name in set_intersected_names:
#            lst_by_world_id = []
#            for key, value in self.__dic_trends.items():
#                dic_trends = value.get_trends()
#                if name in dic_trends:
#                    #lst_by_world_id.append([WORLD_ID_INV[key], dic_trends[name]['tweet_volume']])
#                    lst_by_world_id.append([name, WORLD_ID_INV[key], dic_trends[name]['tweet_volume']])
#            self.__lst_by_name.append(lst_by_world_id)
#            
#        return self.__lst_by_name
    
    def visualize(self, enum_visualization_type, bln_intersected_only=True):
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10,5), dpi=100)
        width = 0.10        
        if bln_intersected_only:
            dic_data = self.intersect_trends()
        else:
            dic_data = self.get_trends_by_name()
        
        
        world_ids = self.get_trend_objects().keys()
        if enum_visualization_type == ENUM_VISUALIZATION_TYPE.BY_WORLD_ID:
            pos = list(range(len(world_ids)))
            counter = 0
            for name, dic_world_id in dic_data.items():
                lst_tweet_volume = []
                for world_id in world_ids:
                    if world_id in dic_world_id:
                        lst_tweet_volume.append(dic_world_id[world_id]['tweet_volume'])
                    else:
                        lst_tweet_volume.append(0)
                axes.bar([p + width*counter for p in pos], lst_tweet_volume, width, label=name)
                for tick in axes.get_xticklabels():
                    tick.set_rotation(90)
                counter += 1
            
            axes.set_xticks([p + (1.5*width) * width for p in pos])
            
            axes.set_xticklabels([WORLD_ID_INV[world_id] for world_id in world_ids])
            axes.set_title('Tweet Volume by World_ID')
            axes.set_ylabel('Tweet Volume')
            axes.set_xlabel('World_ID')        
                
            plt.tight_layout()
            plt.legend(loc=0)
            plt.savefig('test.jpg')
            plt.show()
            
        elif enum_visualization_type == ENUM_VISUALIZATION_TYPE.BY_TWEET_NAME:
            pos = list(range(len(dic_data)))
        else:
            logger.warning('Visualization type not supported - please review `ENUM_VISUALIZATION_TYPE` class.')
            
            
            
    def visualize_trends(self):
        fig, ax = plt.subplots(figsize=(10,5), dpi=1000)
        lst_by_world_id = list(map(list, zip(*self.__lst_by_name)))
        width = 0.25
        pos = list(range(len(lst_by_world_id[0])))
        print(len(lst_by_world_id))
        counter = 0
        for world_id in lst_by_world_id:
            lst_name = []
            lst_volume =[]
            for name in world_id:
                lst_name.append(name[0])
                lst_volume.append(name[2])
            
            print(len(lst_volume))
            print(len(lst_name))
            
            ax.bar([p + width*counter for p in pos], lst_volume, width, label=world_id[0][1])
            for tick in ax.get_xticklabels():
                tick.set_rotation(90)
            
            counter += 1

        print(counter)
        
        ax.set_xticks([p + (1.5*width) * width for p in pos])
        ax.set_xticklabels(lst_name)
        ax.set_title('Intersected Tweets')
        ax.set_ylabel('Tweet Volume')
        ax.set_xlabel('Name')        
            
        plt.tight_layout()
        plt.legend(loc=0)
        plt.savefig('test.jpg')
        plt.show()         
            

    class Trend():
        def __init__(self, 
                     obj_twitter_api,
                     int_world_id):
            self.__obj_twitter_api = obj_twitter_api
            self.__int_world_id = int_world_id
            self.set_data()
            
        def get_data(self):
#            return json.dumps(self.__obj_twitter_api.trends.place(_id=self.__int_world_id), 
#                              indent=1)
            return self.__obj_twitter_api.trends.place(_id=self.__int_world_id)
        
        def set_data(self):
            lst_data = self.get_data()            
            self.__str_as_of = lst_data[0]['as_of']
            self.__str_created_at = lst_data[0]['created_at']
            self.__lst_locations = lst_data[0]['locations']
                        
            dic_data = dict()
            for trend in lst_data[0]['trends']:
                name = trend['name']
                if trend['tweet_volume'] :
                    trend['tweet_volume'] = int(trend['tweet_volume'])
                else:
                    trend['tweet_volume'] = 0
                trend.pop('name')
                dic_data[name] = trend
            
            self.__dic_data = dic_data
            return self.__dic_data
        
        def get_as_of(self, bln_time_format = False):
            if bln_time_format:
                return dateutil.parser.parse(self.__str_as_of)
            else:
                return self.__str_as_of
        
        def get_created_at(self, bln_time_format = False):
            if bln_time_format:
                return dateutil.parser.parse(self.__str_created_at)
            else:
                return self.__str_created_at
        
        def get_locations(self):
            return self.__lst_locations
        
        def get_trends(self):
            return self.__dic_data
            
        

def get_trends(twitter_api, lst_world_id, name_only=False):
    if name_only:
        return [set([trend['name'] 
                for trend in twitter_api.trends.place(_id=world_id)[0]['trends']])
                for world_id in lst_world_id]
    else:
        return [json.dumps(twitter_api.trends.place(_id=world_id), indent=1)
                for world_id in lst_world_id]
    



if __name__ == '__main__':    
    twitter_data = TwitterData()
    twitter_data.add_trends(WORLD_ID['SINGAPORE'])
    twitter_data.add_trends(WORLD_ID['MALAYSIA'])
    
    intersected_trends = twitter_data.intersect_trends()

    
    #trends = get_trends(twitter_data.get_twitter_api(), [WORLD_ID['UNITED_STATES'],WORLD_ID['WORLD']],False)
    #print(*trends)

    
    
#    for tweet in twitter_api.home_timeline():
#        print(tweet.text)
#    trends = get_trends(twitter_api, [WORLD_ID['MALAYSIA'],WORLD_ID['SINGAPORE']],True)
#    print(set.intersection(*trends))
#    
#    q = '#dearmetenyearsago'
#    
#    # see http://dev.twitter.com/docs/api/1.1/get/search/tweets
#    # new https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
#    search_results = twitter_api.search.tweets(q=q)
#    statuses = search_results['statuses']
#    for __ in range(5):
#        print('Length of statuses', len(statuses))
#        try:
#            next_results = search_results['search_metadata']['next_result']
#        except KeyError as e: #No more results when next_results does not exist
#            break
#        
#        # create a dictionary from next_results, which has the following form:
#        # ?max_id = 313519052523986943&q=NCAA&include_entities=1
#        
#        kwargs = dict([kv.split('=') for kv in next_results[1:].split('&')])
#        
#        search_results = twitter_api.search.tweets(**kwargs)
#        statuses += search_results['statuses']
#        
#    # show one sample search result by slicing the list...
#    print(json.dumps(statuses[0], indent=1))
#    print(statuses[0]['text'])
