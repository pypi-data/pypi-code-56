from emora_stdm import DialogueFlow, Macro
from enum import Enum
import json, os
import random
from _globals import TRAVELDIR

class State(Enum):
    START = 0
    OUTDOOR_START = 1
    START_TRAVEL = 2
    END = 100
    ROBOT = 3
    ROBOT_TRAVEL = 4
    ASK_TRAVEL = 5
    GROCERY_STORE = 6
    TRAVEL_N = 7
    TRAVEL_Y = 8
    ROBOT_FOOD = 9
    CITY_DISLIKE = 10
    CITY_NOT_TRAVELED = 11
    CITY_TRAVELED = 12
    ASK_OPINION_REASON = 13
    CITY_DISCUSS = 14
    REASON_NOT_SURE = 15
    REASON_N = 16
    REASON_Y = 17
    ROBOT_FOOD_OPINION = 18
    CITY_TOURISM = 20
    OK_THE_CITY = 21
    NOT_THE_CITY = 22
    ATTRACTION_OPINION = 25
    ATTRACTION_OPINION_D = 26
    ATTRACTION_OPINION_N = 27
    ATTRACTION_OPINION_Y = 28
    CITY_RECOMMEND = 30
    CITY_RECOMMEND_N = 31
    CITY_RECOMMEND_Y = 32
    FOOD_RECOMMEND = 35
    FOOD_RECOMMEND_N = 36
    FOOD_RECOMMEND_Y = 37
    FOOD_OPINION = 40
    FOOD_NOT_KNOW = 41
    FOOD_DISLIKE = 42
    FOOD_LIKE = 43
    ATTRACTION_RECOMMEND = 45
    ATTRACTION_RECOMMEND_D = 46
    ATTRACTION_RECOMMEND_N = 47
    ATTRACTION_RECOMMEND_Y = 48
    USER_REC_CITY = 50
    USER_REC_ANSWER = 51
    USER_REC_NO = 52
    MOVIE_REC = 55
    MOVIE_REC_N = 56
    MOVIE_REC_HAVE_WATCHED = 57
    MOVIE_REC_Y = 58
    MUSIC_REC = 60
    MUSIC_REC_N = 61
    MUSIC_REC_HAVE_HEARD = 62
    MUSIC_REC_Y = 63
    ASK_FAV_CITY = 66
    FAV_SAME = 67
    FAV_END = 68
    FAV_NO = 69
    NO_MATCH = 70
    TRAVEL_PLAN = 75
    TRAVEL_PLAN_D = 76
    TRAVEL_PLAN_Y = 77
    TRAVEL_PLAN_N = 78
    TRAVEL_PET = 80
    TRAVEL_TIME = 81
    TRAVEL_TIME_D = 82
    TRAVEL_TIME_E = 83
    TRAVEL_TIME_L = 84
    TRAVEL_EAT = 86
    TRAVEL_EAT_D = 87
    TRAVEL_EAT_Y = 88
    TRAVEL_EAT_N = 89
    TRAVEL_PET_Y = 92
    TRAVEL_PET_N = 91
    TRAVEL_N_PET = 95
    TRAVEL_N_PET_Y = 97
    TRAVEL_N_PET_N = 96



class TRAVEL_CATCH(Macro):
    """Catch user utterance

    Attribute:
        path: Path of database.
    """

    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        # Catch user utterance in first key
        if len(args) == 0:
            return ngrams & self.db.keys()

        # Catch the user utterance in the third key
        if len(args) == 1:
            return ngrams & self.db[vars[args[0]]].keys()

        # Catch the user utterance in the third key
        if len(args) == 2:
            return ngrams & self.db[vars[args[0]]][vars[args[1]]].keys()


class TRAVEL_RANDOM(Macro):
    """Random generate keys

    Attribute:
        path: Path of database.
    """
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        # Random generate the first key
        name = 'db_keys' + self.path
        name_1 = 'db_keys_1' + self.path
        name_2 = 'db_keys_2' + self.path
        name_3 = 'db_keys_3' + self.path

        if len(args) == 0:
            if vars.get(name) is None or len(vars[name]) == 0:
                vars[name] = list(self.db.keys())
            key = random.choice(vars[name])
            vars[name] = vars[name].remove(key)
            return key

        # Random generate unduplicated the first key
        elif len(args) == 1:
            if vars.get(name_1) is None or len(vars[name_1]) <= 1:
                vars[name_1] = list(self.db[vars[args[0]]].keys())
            if vars[args[0]] in vars[name_1]:
                vars[name_1].remove(vars[args[0]])
            key_1 = random.choice(vars[name_1])
            vars[name_1] = vars[name_1].remove(key_1)
            return key_1

        # Random generate the third key
        elif len(args) == 2:
            if vars.get(name_2) is None or len(vars[name_2]) <= 1:
                vars[name_2] = list(self.db[vars[args[0]]][args[1]].keys())
            key_2 = random.choice(vars[name_2])
            vars[name_2] = vars[name_2].remove(key_2)
            return key_2

        # Random generate unduplicated the third key
        elif len(args) == 3:
            if vars.get(name_3) is None or len(vars[name_3]) <= 1:
                vars[name_3] = list(self.db[vars[args[0]]][vars[args[1]]].keys())
            if vars[args[-1]] in vars[name_3]:
                vars[name_3].remove(vars[args[0]])
            key_3 = random.choice(vars[name_3])
            vars[name_3] = vars[name_3].remove(key_3)
            return key_3


class TRAVEL_DETAIL(Macro):
    """Get keys value

    Attribute:
        path: Path of database.
    """
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as f:
            self.db = json.load(f)

    def run(self, ngrams, vars, args):
        # Get the value of the first key
        if len(args) == 1:
            return self.db[vars[args[0]]]

        # Get the value of the second key
        elif len(args) == 2:
            return self.db[vars[args[0]]][args[1]]

        # Catch the value of the third key
        elif len(args) == 3:
            return self.db[vars[args[0]]][args[1]][vars[args[2]]]


class CATCH_LIST(Macro):
    """Catch user utterance with list.

    Attribute:
        list: A list whether user utterance is in or not.
    """

    def __init__(self, list):
        """Inits CATCH with list"""
        self.list = list

    def run(self, ngrams, vars, args):
        """Performs operation"""
        return ngrams & self.list


# Database
travel_db = TRAVELDIR.replace('__***__','travel_database.json')
city_db = TRAVELDIR.replace('__***__','city_onto.json')

# Variables
TRANSITION_OUT = ["movies", "music", "sports"]
NULL = "NULL TRANSITION"
CITY_IN_THE_LIST = {"honolulu","chicago","miami","orlando","philadelphia","san francisco","new orleans", "washington dc","houston","san diego","las vegas","los angeles","atlanta","seattle","bangkok","london","hong kong","macau","singapore","paris","dubai","kuala lumpur"}
# The cities not in the database
CITY_LIST = {"tokyo","jakarta","chongqing","manila","delhi","seoul","mumbai","shanghai","sao paulo","beijing",
             "lagos","mexico city","guangzhou","dhaka","osaka","cairo","karachi","moscow","chengdu",
             "kolkata","buenos aires","tehran","tianjin","kinshasa","rio de janeiro",
             "baoding", "lahore", "lima", "bangalore", "ho chi minh", "harbin", "wuhan", "shijiazhuang", "bogota", "suzhou",
             "linyi", "chennai", "nagoya", "nanyang", "zhengzhou", "hyderabad", "surabaya", "hangzhou", "johannesburg",
             "quanzhou", "taipei", "dongguan", "bandung", "hanoi", "shenyang", "baghdad", "onitsha",
             "ahmedabad", "luanda", "dallas", "pune", "nanjing", "boston", "santiago",
             "riyadh", "dusseldorf", "madrid", "toronto", "surat"}
YES = {"yes", "yea", "yup", "yep", "i do", "yeah", "a little", "sure", "of course", "i have", "i am", "sometimes", "too", "as well", "also", "agree","good", "keep","why not", "ok", "okay", "fine", "continue", "go on", "definitely", "liked", "loved"}
NO = {"no", "nope", "dont", "nothing", "nuh", "not", "don't", "haven't", "didn't", "doesn't", "never", "shouldn't"}
DONT_KNOW =  {"didn't try", "not sure", "don't know", "wouldn't know", "didn't know", "no idea", "don't remember", "can't recall", "can't remember", "didn't remember", "couldn't recall"}
# Functions
macros = {
    'CATCH': TRAVEL_CATCH(city_db),
    'RANDOM': TRAVEL_RANDOM(travel_db),
    'RANDOM_TOURISM': TRAVEL_RANDOM(travel_db),
    'RANDOM_FOOD': TRAVEL_RANDOM(travel_db),
    'RANDOM_EVENT': TRAVEL_RANDOM(travel_db),
    'RANDOM_CULTURE': TRAVEL_RANDOM(travel_db),
    'CITY_DETAIL': TRAVEL_DETAIL(city_db),
    'DETAIL': TRAVEL_DETAIL(travel_db),
    'CATCH_CITY_LIST': CATCH_LIST(CITY_IN_THE_LIST),
    'CATCH_YES':CATCH_LIST(YES),
    'CATCH_NO':CATCH_LIST(NO),
    'CATCH_NOT_SURE':CATCH_LIST(DONT_KNOW),
    'RANDOM_MUSIC':TRAVEL_RANDOM(travel_db),
    'RANDOM_MOVIE':TRAVEL_RANDOM(travel_db)
}


df = DialogueFlow(State.START, initial_speaker=DialogueFlow.Speaker.USER, macros=macros)

df.add_system_transition(State.START, State.START_TRAVEL,
                         '"I know that travelling to faraway cities may seem risky right now for good reasons. '
                         'But it can still be fun to dream about your future vacation plans. Do you like to travel?"')

# do you like to travel
df.add_user_transition(State.START_TRAVEL, State.TRAVEL_Y,
                       '{#AGREE,[i travel],#EXP(like),[{favorite, hobby, best}]}')
df.add_user_transition(State.START_TRAVEL, State.TRAVEL_N,
                       '{#DISAGREE,[i,not,travel],[not,#EXP(like)],[{hate, worst, dislike, tired, hated}]}')
df.add_user_transition(State.START_TRAVEL, 'travel_unx',
                       '#UNX')

# doesnt like to travel -> end
df.add_system_transition(State.TRAVEL_N, 'travel_n_followup',
                         '"I understand. It can be hard to take time off for a vacation and travelling is often super '
                         'expensive. Honestly, you can just as easily have a good time in your own home and '
                         'there are often fun things to do in the area around where you live. "')
df.add_user_transition('travel_n_followup', State.END, '#UNX')

df.add_system_transition(State.TRAVEL_N, 'travel_n_followup',
                         '"I understand. It can be hard to take time off for a vacation and travelling is often super '
                         'expensive. Plus you have to take care of your pet " $name " anyway. Travelling with pets '
                         'is often pretty hard. "')

# does like to travel
df.add_system_transition(State.TRAVEL_Y, State.TRAVEL_TIME,
                         '"I think travelling is pretty amazing, too! To go to new places and see all of the amazing '
                         'sights is a great experience. So, are you an early-riser during '
                         'a vacation or do you sleep in to be well-rested for the events of each day?"')
df.add_system_transition(State.TRAVEL_Y,State.TRAVEL_PET,
                         '"So, you enjoy travelling? I remember you mentioned that you have a pet. '
                         'Do you usually bring " $pet_name " with you?"', score=2.0)
df.add_system_transition('travel_unx', State.TRAVEL_TIME,
                         '"Personally, I love to travel to see all of the amazing '
                         'sights. When you do travel, are you an early-riser '
                         'or do you sleep in to be well-rested for the events of each day?"')

df.add_user_transition(State.TRAVEL_PET, State.TRAVEL_PET_Y,
                       '{#AGREE,[#NOT(not),{#LEM(come,bring),with},{me,us}],[#NOT(not),#LEM(bring,take),along]}')
df.add_user_transition(State.TRAVEL_PET, State.TRAVEL_PET_N,
                       '{#DISAGREE,[#NOT(not),leave], [#ONT(_related person)], [#LEM(take) care], [#LEM(stay)]}')
df.set_error_successor(State.TRAVEL_PET, State.TRAVEL_PET_N)

df.add_system_transition(State.TRAVEL_PET_Y, State.TRAVEL_TIME,
                         '"Wow, it sounds like " $name " is a lucky animal to be able to travel with you to new places! '
                         'So, are you an early-riser during a vacation or do you sleep in to be well-rested for '
                         'the events of each day?"')
df.add_system_transition(State.TRAVEL_PET_N, State.TRAVEL_TIME,
                         '"I guess it can be better to leave them home when you travel. '
                         'I\'ve heard that a lot of pets are not used to long trips, especially in foreign locations. '
                         'So, are you an early-riser during a vacation or do you sleep in to be well-rested for '
                         'the events of each day?"')

# early riser or sleep in?
df.add_user_transition(State.TRAVEL_TIME,State.TRAVEL_TIME_D,
                       '{#IDK,[{[not,care], no difference, whatever, depends, change, changes, [not,matter], sometimes, both}]}')
df.add_user_transition(State.TRAVEL_TIME,State.TRAVEL_TIME_E,
                       '[{former, early, save time, dawn, sun rise, morning, waste, first, [not,sleep,{in,late,past}]}]')
df.add_user_transition(State.TRAVEL_TIME,State.TRAVEL_TIME_L,
                       '[{latter, second, late, stay, bed, afternoon, noon, night, nightlife, later, [#NOT(not),sleep,in]}]')
df.set_error_successor(State.TRAVEL_TIME,State.TRAVEL_TIME_D)

df.add_system_transition(State.TRAVEL_TIME_E, State.TRAVEL_PLAN,
                         '"I really admire people who can get up early during vacations. '
                         'You must have a lot of discipline. Speaking of which, do you like to plan each step of your '
                         'day or be more spontaneous? "')
df.add_system_transition(State.TRAVEL_TIME_L, State.TRAVEL_PLAN,
                         '"Oh yes! Sleeping in is definitely much easier than getting up early! It\'s also easier to '
                         'not plan every step of your trip. Do you tend to do a lot of planning, or do you do things more '
                         'spontaneously?"')
df.add_system_transition(State.TRAVEL_TIME_D, State.TRAVEL_PLAN,
                         '"Being flexible is definitely an admirable trait! '
                         'Speaking of which, do you like to plan each step of your day or be more spontaneous about it?"')

# planner or spontaneous?
df.add_user_transition(State.TRAVEL_PLAN,State.TRAVEL_PLAN_Y,
                       '{#AGREE,[{plan, ahead, planner, before, former, first, work, [#NOT(not),in detail]}]}')
df.add_user_transition(State.TRAVEL_PLAN,State.TRAVEL_PLAN_N,
                       '{#DISAGREE,[{latter, second, chance, flow, spontaneous, spontaneously, surprise, do whatever}]}')
df.add_user_transition(State.TRAVEL_PLAN,State.TRAVEL_PLAN_D,
                       '{#IDK,[{not every step, not each step, between, mostly, sometimes, both}]}')
df.set_error_successor(State.TRAVEL_PLAN, State.TRAVEL_PLAN_D)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

df.add_system_transition(State.TRAVEL_PLAN_Y, State.TRAVEL_EAT,
                         '"wow respect, i really wanna have a travel buddy that makes plans before traveling. '
                         'I cant do it by myself. '
                         'What about food? Would you rather linger over meals or scarf them down and get moving again? "')
df.add_system_transition(State.TRAVEL_PLAN_N, State.TRAVEL_EAT,
                         '"yeah me too! but i really wanna have a travel buddy that makes some plans before traveling. '
                         'What about food? Would you rather linger over meals or scarf them down and get moving again?"')
df.add_system_transition(State.TRAVEL_PLAN_D, State.TRAVEL_EAT,
                         '"same! i would do some work before hand but not every step. '
                         'What about food? Would you rather linger over meals or scarf them down and get moving again?"')

# enjoy food or a chore

df.add_user_transition(State.TRAVEL_EAT,State.TRAVEL_EAT_D,'[{#CATCH_NOT_SURE(), depends, sometimes, quality, maybe, not sure, sometimes, both, also}]')
df.add_user_transition(State.TRAVEL_EAT,State.TRAVEL_EAT_Y,'[{first, linger, like, enjoy, local, try, former, food, foodie, all about, cuisine}]')
df.add_user_transition(State.TRAVEL_EAT,State.TRAVEL_EAT_N,'[{latter, finish, car, snack, second, moving, scarfing, swallow, swallowing, waste of time}]')
df.set_error_successor(State.TRAVEL_EAT, State.TRAVEL_EAT_D)

df.add_system_transition(State.TRAVEL_EAT_Y, State.ASK_TRAVEL, '"Same here, I am a giant foodie and every time I go to a new place I look for new foods to try. One of my favorite cities is"$city={honolulu, chicago, miami, orlando, philadelphia, san francisco, new orleans, washington dc, houston, san diego, las vegas, los angeles, atlanta, bangkok, london, hong kong, macau, singapore, paris, dubai, kuala lumpur}"."#DETAIL(city, brief_intro)"I was planning on traveling to there but my trip was cancelled due to this pandemic. Have you ever been to this city before?"')
df.add_system_transition(State.TRAVEL_EAT_N, State.ASK_TRAVEL, '"Oh ok. For some people, enjoy the scenery and local culture is more important. One of my favorite cities is"$city={honolulu, chicago, miami, orlando, philadelphia, san francisco, new orleans, washington dc, houston, san diego, las vegas, los angeles, atlanta, bangkok, london, hong kong, macau, singapore, paris, dubai, kuala lumpur}"."#DETAIL(city, brief_intro)"I was planning on traveling to there but my trip was cancelled due to this pandemic. Have you ever been to this city before?"')
df.add_system_transition(State.TRAVEL_EAT_D, State.ASK_TRAVEL,'"Yeah it really depends on the state of mind and time. One of my favorite cities is"$city={honolulu, chicago, miami, orlando, philadelphia, san francisco, new orleans, washington dc, houston, san diego, las vegas, los angeles, atlanta, bangkok, london, hong kong, macau, singapore, paris, dubai, kuala lumpur}"."#DETAIL(city, brief_intro)"I was planning on traveling to there but my trip was cancelled due to this pandemic. Have you ever been to this city before? "')

df.add_user_transition(State.ASK_TRAVEL, State.CITY_DISLIKE, '[{hate, worst, dislike, tired, hated, didnt}]')
df.add_user_transition(State.ASK_TRAVEL, State.CITY_NOT_TRAVELED, '[{#CATCH_NO(), havent, never}]')
df.add_user_transition(State.ASK_TRAVEL, State.CITY_TRAVELED, '[{#CATCH_YES(), love, like, favorite, hobby, best, good, hometown, grew up, work, live, here}]')
df.add_user_transition(State.ASK_TRAVEL, State.ROBOT_TRAVEL, '[{robot, bot}]')
df.set_error_successor(State.ASK_TRAVEL, State.CITY_NOT_TRAVELED)

df.add_system_transition(State.ROBOT_TRAVEL, State.ASK_TRAVEL,'"i can do things i like in my virtual world. have you been to "$city" before? "')
df.add_system_transition(State.CITY_DISLIKE, State.CITY_RECOMMEND, '"Oh really? Maybe I should consider a different city. Do you have any city in mind that you would recommend me to go to?"')
df.add_system_transition(State.CITY_NOT_TRAVELED, State.CITY_DISCUSS, '"Oh thats fine. I love it because I heard that"#DETAIL(city, reason_for_travel)" I also love its food, culture, and I even know some of its tourist attractions. do you want to go there one day?"')
df.add_system_transition(State.CITY_TRAVELED, State.ASK_OPINION_REASON, '{Thats nice, Yay}"! then I can ask you opinions on this before I go. I heard that "#DETAIL(city, reason_for_travel)" Is that right?"')

df.add_user_transition(State.ASK_OPINION_REASON,State.REASON_NOT_SURE,'[{#CATCH_NOT_SURE(), dont know, no idea, who knows, not sure, not quite sure}]')
df.add_user_transition(State.ASK_OPINION_REASON,State.REASON_N, '[{#CATCH_NO(), havent, never}]')
df.add_user_transition(State.ASK_OPINION_REASON,State.REASON_Y, '[{#CATCH_YES(), love, like, favorite, best, good}]')
df.add_user_transition(State.ASK_OPINION_REASON, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.ASK_OPINION_REASON, State.REASON_NOT_SURE)

df.add_user_transition(State.CITY_DISCUSS,State.NOT_THE_CITY, '[{#CATCH_NO(), never}]')
df.add_user_transition(State.CITY_DISCUSS,State.OK_THE_CITY,'[{#CATCH_YES(), love, like, favorite, best, good, i would, maybe, might}]')
df.add_user_transition(State.CITY_DISCUSS, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.CITY_DISCUSS, State.OK_THE_CITY)

df.add_user_transition(State.CITY_RECOMMEND,State.CITY_RECOMMEND_N,'[{#CATCH_NO(), never}]')
df.add_user_transition(State.CITY_RECOMMEND,State.CITY_RECOMMEND_Y,'[{#CATCH_YES(), love, like, favorite, best, good, i would}]')
df.add_user_transition(State.CITY_RECOMMEND, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.CITY_RECOMMEND,State.CITY_RECOMMEND_N)

df.add_system_transition(State.REASON_NOT_SURE,State.FOOD_OPINION, '"Ah ok. I will take that into consideration. Thanks! I also want to try out the food there. i know some of their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}". If you have tried it there, did you like it?"')
df.add_system_transition(State.REASON_N,State.CITY_RECOMMEND, '"Oh no, thats sad. I wanted to go because of that. Do you have any city in mind that you would recommend me to go to?"')
df.add_system_transition(State.REASON_Y,State.ATTRACTION_OPINION,'"Good to know! I know they have "$tourism={#RANDOM_TOURISM(city, tourist_attraction)}" which is quite popular. I actually wanna go there. Would you recommend the place?"')
df.add_system_transition(State.NOT_THE_CITY, State.FOOD_RECOMMEND,'"Ah thats okay. After all, it is better for us to stay home for now. One of my favorite cities also includes "$city={seattle, new york}", because"#DETAIL(city, reason_for_travel)" but it is undergoing a huge crisis right now. I hope everything will get better soon. Besides, I love their "$food={#RANDOM_FOOD(city, famous_food)}". Would you like to try that there one day."')
df.add_system_transition(State.OK_THE_CITY,State.FOOD_RECOMMEND,'"Yay! We have the same wishes now! But I bet I know more about this city than you do. For example, i know some of their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}". You should definitely try if you go there one day!"')
df.add_system_transition(State.CITY_RECOMMEND_N,State.END,'"Well thats fine. I am sure both of us will find a place that each will enjoy. "')
df.add_system_transition(State.CITY_RECOMMEND_Y,State.USER_REC_CITY,'"Thanks for your recommendation！I will take that into consideration. Do you want to tell me more about the city?"')

df.add_user_transition(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_D,'[{#CATCH_NOT_SURE(), dont know, no idea, who knows, not sure, not quite sure, never been}]')
df.add_user_transition(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_N,'[{#CATCH_NO(), never, shouldnt}]')
df.add_user_transition(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_Y,'[{#CATCH_YES(), love, like, favorite, best, good, i would, fine}]')
df.add_user_transition(State.ATTRACTION_OPINION, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.ATTRACTION_OPINION,State.ATTRACTION_OPINION_D)

df.add_user_transition(State.FOOD_RECOMMEND,State.FOOD_RECOMMEND_N, '[{#CATCH_NO(), never, shouldnt, wont, wouldnt}]')
df.add_user_transition(State.FOOD_RECOMMEND,State.FOOD_RECOMMEND_Y, '[{#CATCH_YES(), love, like, favorite, best, good, i would, fine, delicious, tasty, maybe}]')
df.add_user_transition(State.FOOD_RECOMMEND,State.ROBOT_FOOD, '[{robot, bot}]')
df.set_error_successor(State.FOOD_RECOMMEND,State.FOOD_RECOMMEND_N)

df.add_user_transition(State.USER_REC_CITY, State.USER_REC_ANSWER,'[{#CATCH_YES(), love, like, favorite, best, good, i would, fine, delicious, tasty, maybe, temperature, weather, beach, culture, event, people, nice}]')
df.add_user_transition(State.USER_REC_CITY, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.USER_REC_CITY, State.USER_REC_NO)

df.add_system_transition(State.ROBOT_FOOD, State.ATTRACTION_RECOMMEND,'"I may not live physically in your world, but I do eat food in mine. Anyways, I also know they have the tourist attraction "$tourism={#RANDOM_TOURISM(city, tourist_attraction)}"which is quite popular. I actually wanna go there. "$tourism","#DETAIL(city, tourist_attraction, tourism)" Would you consider this could be a good place to visit? "')
df.add_system_transition(State.USER_REC_ANSWER, State.END,'"Nice nice! I will definitely look into it. Thanks again! "')
df.add_system_transition(State.USER_REC_NO, State.END,'"Ok but still thanks again! "')
df.add_system_transition(State.ATTRACTION_OPINION_Y,State.FOOD_OPINION, '"Nice! I will definitely go one day once everything is fine. I also want to try out the food there. i know some of their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}", which, "#DETAIL(city, famous_food, food)". If you have tried it there, did you like it?"')
df.add_system_transition(State.ATTRACTION_OPINION_N,State.FOOD_OPINION, '"Ah ok. I will take that into consideration. Thanks! I also want to try out the food there. i know some of their popular cuisines such as "$food={#RANDOM_FOOD(city, famous_food)}", which, "#DETAIL(city, famous_food, food)". If you have tried it there, did you like it?"')
df.add_system_transition(State.ATTRACTION_OPINION_D,State.FOOD_OPINION, '"Okay, thats fine. I also want to try out the food there. i know some of their popular cuisines such as"$food={#RANDOM_FOOD(city, famous_food)}", which ,"#DETAIL(city, famous_food, food)". If you have tried it there, did you like it?"')

df.add_system_transition(State.FOOD_RECOMMEND_Y,State.ATTRACTION_RECOMMEND, '"Good to know! I also know they have the tourist attraction"$tourism={#RANDOM_TOURISM(city, tourist_attraction)}"which is quite popular. I actually wanna go there. "$tourism","#DETAIL(city, tourist_attraction, tourism)" Would you consider this could be a good place to visit?"' )
df.add_system_transition(State.FOOD_RECOMMEND_N,State.ATTRACTION_RECOMMEND,'"haha thats fine. maybe we dont share the same taste. I also know they have the tourist attraction"$tourism={#RANDOM_TOURISM(city, tourist_attraction)}"which is quite popular. I actually wanna go there. "$tourism","#DETAIL(city, tourist_attraction, tourism)" Would you consider this could be a good place to visit?"' )

df.add_system_transition(State.FOOD_NOT_KNOW,State.MOVIE_REC,'"oh ok. I will try it myself then. Hopefully it will turn out to be good. I first heard about this city because of the movie "$movie={#RANDOM_MOVIE(city, movie)}". Do you know of this movie?"')
df.add_system_transition(State.FOOD_LIKE,State.MOVIE_REC,'"Awesome, I have found the right person to ask! I will try once I get there. I first heard about this city because of the movie "$movie={#RANDOM_MOVIE(city, movie)}". Do you know of this movie?"')
df.add_system_transition(State.FOOD_DISLIKE, State.MOVIE_REC,'"oh no. that\'s ok. i will look for something else to eat then. I first heard about this city because of the movie "$movie={#RANDOM_MOVIE(city, movie)}". Do you know of this movie?"')

df.add_user_transition(State.FOOD_OPINION,State.FOOD_NOT_KNOW,'[{#CATCH_NOT_SURE(), dont know, havent, no idea, who knows, not sure, not quite sure, never been, never tried, never had it}]')
df.add_user_transition(State.FOOD_OPINION,State.FOOD_DISLIKE,'[{#CATCH_NO(), never, shouldnt, wont, wouldnt, didnt, hated, not that good, gross, no}]')
df.add_user_transition(State.FOOD_OPINION,State.FOOD_LIKE,'[{#CATCH_YES(), love, like, favorite, best, good, i would, delicious, tasty, maybe, great, good, wonderful, should be}]')
df.add_user_transition(State.FOOD_OPINION,State.ROBOT_FOOD_OPINION, '[{robot, bot}]')
df.set_error_successor(State.FOOD_OPINION,State.FOOD_NOT_KNOW)

df.add_user_transition(State.ATTRACTION_RECOMMEND,State.ATTRACTION_RECOMMEND_N,'[{#CATCH_NO(), shouldnt, wont, wouldnt, not really, else, elsewhere}]')
df.add_user_transition(State.ATTRACTION_RECOMMEND,State.ATTRACTION_RECOMMEND_Y,'[{#CATCH_YES(), love, like, favorite, best, good, i would, fine}]')
df.add_user_transition(State.ATTRACTION_RECOMMEND, State.ROBOT, '[{robot, bot}]')
df.set_error_successor(State.ATTRACTION_RECOMMEND, State.ATTRACTION_RECOMMEND_Y)

df.add_system_transition(State.ROBOT_FOOD_OPINION,State.MOVIE_REC, '"I may not live physically in your world, but I do eat food in mine. Anyways, I first heard about "$city" because of the movie "$movie={#RANDOM_MOVIE(city, movie)}".have you heard about it?"')
df.add_system_transition(State.ATTRACTION_RECOMMEND_N,State.MOVIE_REC, '"Well, thats fine.  I first heard about it because of the movie "$movie={#RANDOM_MOVIE(city, movie)}".have you heard about it?"')
df.add_system_transition(State.ATTRACTION_RECOMMEND_Y,State.MOVIE_REC, '"Thanks for your suggestion. I first heard about it because of the movie "$movie={#RANDOM_MOVIE(city, movie)}".have you heard about it?"')

df.add_user_transition(State.MOVIE_REC, State.MOVIE_REC_N, '[{#CATCH_NO(), music, songs, what is it, what was it, never heard, when, where}]')
df.add_user_transition(State.MOVIE_REC, State.MOVIE_REC_HAVE_WATCHED, '[{did watch, watched}]')
df.add_user_transition(State.MOVIE_REC, State.MOVIE_REC_Y, '[{#CATCH_YES(), did}]')
df.set_error_successor(State.MOVIE_REC, State.MOVIE_REC_N)

df.add_system_transition(State.MOVIE_REC_N, State.ASK_FAV_CITY, '"well,"$movie" "#DETAIL(city, movie, movie)" maybe you could check it out sometime. we have been talk about my favorite city, may i ask what is yours?"')
df.add_system_transition(State.MOVIE_REC_HAVE_WATCHED, State.MUSIC_REC, '"i am glad that we shared some similar experience. to be honest, "$city" always reminds me of the song "$music={#RANDOM_MUSIC(city, music)}". the song "#DETAIL(city, music, music)" you should check it out sometime."')
df.add_system_transition(State.MOVIE_REC_Y,State.MUSIC_REC,'"yay! by watching the movie i kinda feel like i am traveling. to be honest, "$city" always reminds me of the song "$music={#RANDOM_MUSIC(city, music)}". the song "#DETAIL(city, music, music)" you should check it out sometime."')

df.add_user_transition(State.MUSIC_REC, State.MUSIC_REC_HAVE_HEARD, '[{like, liked, love, loved, listened, good, great}]')
df.add_user_transition(State.MUSIC_REC, State.MUSIC_REC_Y, '[{#CATCH_YES(), ok, i might, maybe}]')
df.add_user_transition(State.MUSIC_REC, State.MUSIC_REC_N, '[{#CATCH_NO()}]')

df.set_error_successor(State.MUSIC_REC, State.MUSIC_REC_N)

df.add_system_transition(State.MUSIC_REC_HAVE_HEARD, State.ASK_FAV_CITY,'"wow nice! we have been talk about my favorite city, may i ask what is yours?"')
df.add_system_transition(State.MUSIC_REC_Y, State.ASK_FAV_CITY,'"good! we have been talk about my favorite city, what is your favorite city?"')
df.add_system_transition(State.MUSIC_REC_N, State.ASK_FAV_CITY,'"haha fine! we have been talk about my favorite city, what is your favorite city?"')

df.add_user_transition(State.ASK_FAV_CITY, State.FAV_SAME, '[$fav_city=#CATCH_CITY_LIST()]')
df.add_user_transition(State.ASK_FAV_CITY, State.FAV_END, '[$fav_city=#CATCH()]')
df.add_user_transition(State.ASK_FAV_CITY,State.FAV_NO,'[{#CATCH_NO(),#CATCH_NOT_SURE()}]')
df.set_error_successor(State.ASK_FAV_CITY,State.NO_MATCH)

df.add_system_transition(State.FAV_SAME, State.END, '"wow "$fav_city" is also on the top of my list, maybe we should talk about it next time!"') #because "#DETAIL(city, reason_for_travel)" "$city=$fav_city"
df.add_system_transition(State.FAV_END,State.END,'"aww glad to know that. however, I do not know much about "$fav_city", i only know it is in "$fav_city_state=#CITY_DETAIL(fav_city, state)"."')
df.add_system_transition(State.FAV_NO,State.END,'"ah ok, thats fine"')
df.add_system_transition(State.NO_MATCH, State.END,'"I am not really familiar with it."')

df.update_state_settings(State.END, system_multi_hop=True)


if __name__ == '__main__':
    #df.precache_transitions()
    df.run(debugging=False)

