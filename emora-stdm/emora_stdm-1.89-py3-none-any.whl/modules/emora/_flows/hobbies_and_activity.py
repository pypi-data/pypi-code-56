
from _globals import PATHDIR
from emora_stdm import DialogueFlow


hobby = DialogueFlow('_local_start')
hobby.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
hobby.add_system_transition('_local_start', 'start', '')


system = {
    'state': 'start',
    'enter': '#GCOM(hobby) #GOAL(hobby)',

    '#DEFAULT': 'SYSTEM:root',

    '`So tell me, what did you do today?` '
    '#GATE':
    {
        'state': 'learn_about_day',
        'score': 2,
        'error': {
            '"Okay, I see. Thanks for sharing that with me. "': {
                'score': 2.0,
                'state': 'exit'
            }
        },

        "{" 
        "[#ONT(not), {talk, talking, discuss, discussing, share, sharing, tell, say}]," 
        "[none,your,business]," 
        "[!{[!that,is],thats},private]" 
        "}":{
            'score':3.0,
            '"Okay, it seems like you don\'t want to share that with me. That\'s alright, I hope we can find something '
            'interesting that you do want to talk about, instead. "': 'exit'
        },

        '[#NOT(#ONT(not)),$chore=#ONT(chore)]': {
            '"Oh, you did some chores? '
            'Now that we have all of this time on our hands, '
            'I can imagine it would be nice to tidy up!"': 'exit'
        },

        '[#NOT(#ONT(not)),{#EXP(travel),#LEM(do)},$errand_dest=#ONT(errand)]': {
            'score': 2.0,
            '[!"You know, it may not be the most exciting thing, but '
            'I bet you are glad to be done with that errand for now."]':
            {
                'error': {
                    '"Well, okay. I just know that a lot of people are usually happy to be done with errands. '
                    'Anyways, "': 'exit'
                },
                "{#AGREE,[!{[!i,am],im},#NOT(#ONT(not))],[im,#NOT(#ONT(not)),#EXP(happy)]}": {
                    '"Great! Well, hopefully we can find something interesting to talk about to '
                    'spice up your day, something more exciting than errands. "': 'exit'
                },

                "{"
                "[i,#NOT(#ONT(not)),#EXP(enjoy),{it,that,#LEM(chore),#ONT(errand)}],"
                "[{it,its,that,#LEM(chore),#ONT(errand),they},#NOT(#ONT(not)),{#EXP(fun),#EXP(break)}]"
                "}": {
                    '[!"You enjoy doing errands? I was not really expecting that! '
                    'Let\'s try to continue your pleasant day. "]': 'exit'
                },

                "{#DISAGREE,[!{[!i,am],im},#ONT(not)],[im,#ONT(not),#EXP(happy)]}": {
                    '"I think I heard you say you are not glad to be done with your errands? Well, I am glad '
                    'they seem to bring you some sort of joy. "': 'exit'
                },

                "{"
                "[i,#ONT(not),#EXP(enjoy),{it,that,chore,#ONT(errand)}],"
                "[{it,its,that,#LEM(chore),#ONT(errand),they},#ONT(not),{#EXP(fun),#EXP(break)}],"
                "[{#EXP(annoy),#EXP(hate)}]"
                "}": {
                    '[!"Yeah, errands can be a bit annoying, but you have to do them at some point, unfortunately. '
                    'Let\'s talk about something a bit more exciting, I am sure this is not a very interesting '
                    'topic for you! "]': 'exit'
                }
            }
        },

        '[#NOT(#ONT(not)),$homework=#EXP(homework)]': {
            'score': 3.0,
            '[!"You have some " $homework "? That is a pretty good use of your time, keep up the good work! I know it might be kind of hard to stay motivated due to the current situation. Are you taking a break now?"]':
            {
                "{#AGREE,[!{[!i,am],im},#NOT(#ONT(not))]}":{
                    '"Awesome! I am glad you have decided to include me in your break. "': 'exit'
                },
                "{#DISAGREE,[!{[!i,am],im},#ONT(not)]}":{
                    '"You aren\'t really taking a break, but you are talking to me right now? '
                    'Well, I am glad to be talking to you. "': 'exit'
                },
                "{[should,still,#LEM(do,work)],"
                "[{shouldnt,should not},#LEM(stop,end,finish)]}":{
                    '"You feel like you still should be working on it? Sometimes, you will work even better after taking '
                    'a small break, but yeah, make sure you don\'t neglect your work, for sure. "': 'exit'
                },
                "[{[!{sort,kind},of],maybe,a little,i guess}]":{
                    '"Even a small break can be helpful to refresh you. "': 'exit'
                },
                'error': {
                    '"Regardless, I am glad you have decided to talk with me. It keeps my days interesting, and I hope '
                    'it brings something new and fun to your day too! "': 'exit'
                }
            },

            '#GATE(schoolv:None) #SET($schoolv=True) [!"You have some " $homework "? I\'m actually a student too. "]': {
                'state': "school:ask_like_school",
                'score': 2.0
            }
        },

        '[#NOT(#ONT(not)),#LEM(complete,finish),$homework=#EXP(homework)]': {
            '"It sounds like you finished some work. You should be proud! It feels good to be done, doesn\'t it?"':{
                'error': {
                    '"I see. It does seem like a lot of people are so relieved when they are done with some work. "': 'exit'
                },
                "{#AGREE,[!{[!i,am],im},#NOT(#ONT(not))],[im,#NOT(#ONT(not)),#EXP(happy)]}": {
                    '"I knew it! Well, hopefully we can find something interesting to talk about to '
                    'spice up your day, other than your homework. "': 'exit'
                },

                "{"
                "[i,#NOT(#ONT(not)),#EXP(enjoy),{it,that,#EXP(homework)}],"
                "[{it,its,that,they,#EXP(homework)},#NOT(#ONT(not)),{#EXP(fun),#EXP(break)}]"
                "}": {
                    '"You enjoy doing some schoolwork? Yeah, I guess depending on the topic, it could be cool!"': 'exit'
                },

                "{#DISAGREE,[!{[!i,am],im},#ONT(not)],[im,#ONT(not),#EXP(happy)]}": {
                    '"I think I heard you say you are not glad to be done with your work? Either you enjoy it or '
                    'you still have more to do. Regardless, I am happy to be talking to you now. So, "': 'exit'
                },

                "{"
                "[i,#ONT(not),#EXP(enjoy),{it,that,#EXP(homework)}],"
                "[{it,its,that,they,#EXP(homework)},#ONT(not),{#EXP(fun),#EXP(break)}],"
                "[#EXP(annoy)]"
                "}": {
                    '"Yeah, I think most people find schoolwork to be annoying, but you have to do them at some point, unfortunately. "': 'exit'
                },

                "[{[!{sort,kind},of],maybe,a little,i guess}]": {
                    '"Even if it was just something small that you finished, you should feel proud of yourself! "': 'exit'
                }
            },

            '#GATE(schoolv:None) #SET($schoolv=True) "It sounds like you finished some work. You should be proud! I\'m actually a student too. "': {
                'state': "school:ask_like_school",
                'score': 2.0
            }
        },

        '[#NOT(#ONT(not)),{#EXP(travel),#LEM(attend,do,have)},{school,#EXP(class)}]': {
            'score': 2.0,
            '"Attending class is pretty different at the moment, but I am glad to hear that they are at least '
            'still working for you. "': 'exit',

            '#GATE(schoolv:None) #SET($schoolv=True) "I\'m glad to hear you can still attend class in some form. I\'m actually a student too. "': {
                'state': "school:ask_like_school",
                'score': 2.0
            }
        },

        '[#NOT(#ONT(not)),{[{#EXP(travel),#LEM(do,have)},#LEM(work,job)],#LEM(work)}]': {
            'score': 2.0,
            '"I am glad you are able to keep working in spite of everything that is going on. "': 'exit',
            '#GATE(worklifev:None) #SET($worklifev=True) "I\'m glad you are able to keep working in spite of everything that is going on. "': {
                'state': "worklife:entry_to_happy_work",
                'score': 2.0
            }
        },

        '[#NOT(#ONT(not)),#EXP(travel),$dest=#ONT(indoor_destination)]': {
            'score': 4.0,
            '[!"People haven\'t really been going to the "$dest" recently. It probably '
            'felt good to get out of the house, even for a little bit, but I hope you are staying safe. "]': 'exit'
        },

        '[#NOT(#ONT(not)),{#EXP(travel),#LEM(play)},$dest=#ONT(outdoor_destination)]': {
            'score': 4.0,
            '[!"It is nice to get out of the house and spend some time outdoors in the "$dest", with everything '
            'that is going on. I hope you enjoyed yourself and are staying safe. "]': 'exit'
        },

        '[#NOT(#ONT(not)),{#EXP(travel),#LEM(play)},{outdoors,outdoor,outside}]': {
            'score': 4.0,
            '[!"It is nice to get out of the house and spend some time outdoors, with everything '
            'that is going on. I hope you enjoyed yourself and are staying safe. "]': 'exit'
        },

        '[#NOT(#ONT(not)),{#EXP(travel),#LEM(play)},{indoor,indoors,inside}]': {
            'score': 4.0,
            '[!"I hope you enjoyed your indoor activities, it is good to keep yourself entertained! "]': 'give_fun_activity'
        },

        '[#NOT(#ONT(not)),#LEM(play),{game,games,house,home,dolls,doll,barbie,barbies,toy,toys}]': {
            '[!"I hope you enjoyed playing with your toys, it is good to keep yourself entertained! "]': 'give_fun_activity'
        },

        '[#NOT(#ONT(not)),#LEM(play),$console=#ONT(game_console)]': {
            '[!"Oh, cool! You have a "$console"? I bet you are having a lot of fun playing video games to pass '
            'the time. Are you playing them more than usual nowadays?"]': {
                'error': {
                    '"I see. Video games do seem to be one popular activity to relax and have fun for a lot '
                    'of people. "': 'exit'
                },
                "{#AGREE,[!{[!i,am],im},#NOT(#ONT(not))],[#NOT(#ONT(not)),{more,a lot,#EXP(frequently)}]}": {
                    '"That makes sense. They are one easy way to keep yourself busy at home. "': 'exit'
                },

                "{#DISAGREE,[!{[!i,am],im},#ONT(not)],[#ONT(not),{more,a lot,#EXP(frequently)}]}": {
                    '"Well, I am glad you are able to enjoy playing them at least some of the time. "': 'exit'
                }
            }
        },

        '[#NOT(#ONT(not)),#LEM(play),{#ONT(vgames),[!video, #LEM(game)]}]': {
            '[!"Oh, cool! I bet you are having a lot of fun playing video games to pass '
            'the time. Are you playing them more than usual nowadays?"]': {
                'error': {
                    '"I see. Video games do seem to be one popular activity to relax and have fun for a lot '
                    'of people. "': 'exit'
                },
                "{#AGREE,[!{[!i,am],im},#NOT(#ONT(not))],[#NOT(#ONT(not)),{more,a lot,#EXP(frequently)}]}": {
                    '"That makes sense. They are one easy way to keep yourself busy at home. "': 'exit'
                },

                "{#DISAGREE,[!{[!i,am],im},#ONT(not)],[#ONT(not),{more,a lot,#EXP(frequently)}]}": {
                    '"Well, I am glad you are able to enjoy playing them at least some of the time. "': 'exit'
                }
            }
        },

        '[#NOT(#ONT(not)),{$exercise={#EXP(exercise),[!#LEM(work),out],#ONT(outdoor_exercise,indoor_exercise)},[#LEM(play),$exercise=#ONT(sports)]}]':{
            'score':3.0,
            '[!"Oh, "$exercise"? It seems like a lot of people are spending this extra time at home getting into a '
            'good exercise routine. Is that something you are trying to do too?"]':{
                'error': {
                    '"Ok, sure. Any exercise is better than none!"': 'exit'
                },
                "{"
                "#AGREE,[!{[!i,am],im},#NOT(#ONT(not))],"
                "[#NOT(#ONT(not)),{it,that,some,{#EXP(exercise),[!#LEM(work),out],#ONT(outdoor_exercise,indoor_exercise,sports)}},{more,a lot,#EXP(frequently)}]"
                "}": {
                    '"Wow, I admire you for doing that. It is important to stay healthy in times like this, for sure. "': 'exit'
                },

                "{"
                "#DISAGREE,[!{[!i,am],im},#ONT(not)],"
                "[#ONT(not),{it,that,some,{#EXP(exercise),[!#LEM(work),out],#ONT(outdoor_exercise,indoor_exercise,sports)}},{more,a lot,#EXP(frequently)}]"
                "}": {
                    '"Well, you never know. You just might get into a really good routine anyways, without even trying. "': 'exit'
                },

                "[{[!{sort,kind},of],maybe,a little,i guess}]":{
                    '"Even doing just a little bit of exercise on a regular basis can help. "': 'exit'
                },
            }
        },

        '[#NOT(#ONT(not)),$watching={#EXP(television),#EXP(hbo),#LEM(movie,channel,show,cartoon),youtube,netflix,hulu}]': {
            '[!"Oh, "$watching"? That seems to be a good one. Watching movies and shows is always so fun, and '
            'an easy way to relax. "]': 'exit'
        },

        '[#NOT(#ONT(not)),#LEM(see,talk,chat,call),$contact=#ONT(related_person)]': {
            '[!"It is good to hear that you are keeping in touch with the people in your life. '
            'Are you close to your"$contact"?"]':{
                'error': {
                    '"Okay. Well, I hope you are able to stay connected with everyone you want to, even in these weird times. "': 'exit'
                },
                "{#AGREE,[!{[!i,am],im},#NOT(#ONT(not))],[#NOT(#ONT(not)),{#LEM(close),intimate,inseparable,best}]}": {
                    '"Wow, you sound like you are really close to them. I am glad to hear that. "': 'exit'
                },

                "{#DISAGREE,[!{[!i,am],im},#ONT(not)],[#ONT(not),{#LEM(close),intimate,inseparable,best}]}": {
                    '"You aren\'t that close to them? Well, I hope you are able to stay connected with the other people '
                    'who are important in your life. "': 'exit'
                }
            }
        },

        '[#NOT(#ONT(not)),#LEM(play),with,$contact=#ONT(related_person)]': {
            '[!"It is good to hear that you are spending time with the people in your life. '
            'Are you close to your"$contact"?"]': {
                'error': {
                    '[!"Okay. Well, playing with your" $contact "is a good way to pass the time and have some fun, I think."]': 'exit'
                },
                "{#AGREE,[!{[!i,am],im},#NOT(#ONT(not))],[#NOT(#ONT(not)),{#LEM(close),intimate,inseparable,best}]}": {
                    '"Wow, you sound like you are really close to them. I am glad to hear that. "': 'exit'
                },

                "{#DISAGREE,[!{[!i,am],im},#ONT(not)],[#ONT(not),{#LEM(close),intimate,inseparable,best}]}": {
                    '"You aren\'t that close to them? Well, I hope you are able to spend time with the other people '
                    'who are important in your life, too. "': 'exit'
                }
            }
        },

        '[#NOT(#ONT(not)),#LEM(play),with,$animal=#ONT(animal)]': {
            '[!"It is good to hear that you are spending time with your animals. '
            'Do you play a lot with your "$animal"?"]': {
                'error': {
                    '[!"Okay. Well, playing with your" $animal "is a good way to pass the time and have some fun, I think."]': 'exit'
                },
                "{#AGREE,[!{[!i,am],im},#NOT(#ONT(not))],[#NOT(#ONT(not)),{#LEM(close),intimate,inseparable,best}]}": {
                    '"Wow, you sound like you really care for them. I am glad to hear that. "': 'exit'
                },

                "{#DISAGREE,[!{[!i,am],im},#ONT(not)],[#ONT(not),{#LEM(close),intimate,inseparable,best}]}": {
                    '"You don\'t spend that much time playing with your " $animal "? Well, it is always good to give '
                    'them some attention when you can."': 'exit'
                }
            }
        },

        "[$hobby=#ONT(hobby)]": {
            '[!"Oh, okay. I heard you say"$hobby". That is a great thing to do to keep yourself busy, especially in these times! "]': 'exit'
        },

        '{#IDK,[{nothing,none,have not decided,havent decided, up in the air, undecided, not much,[#ONT(not),anything]}]}':{
            '{"Yeah, sometimes it is hard to decide what to do.",'
            '"Sure, I know the feeling of not really doing too much."}': {
                'score': 2.0,
                'state': 'give_fun_activity'
            }
        },

        '[#NOT(#ONT(not)),{relax,chill,fun,enjoy,[#LEM(take),break]}]':{
            '{"Its always good to take some time to relax.",'
            '"You can never underappreciate the value of taking some time for yourself."}':  {
                'score': 2.0,
                'state': 'give_fun_activity'
            }
        },

        "[{"
        "#LEM(quarantine,isolate),"
        "shelter in place,"
        "[#LEM(stuck,stay,trap,confine) #LEM(home,inside,indoor,indoors,house,apartment,home)],"
        "#LEM(survive)"
        "}]":{
            'score':3.0,
            '"It sounds like the coronavirus has changed up your lifestyle quite a bit. I hope your transition has been relatively smooth. "': 'exit'
        },

        "[#LEM(stock,find,get,buy,purchase),#LEM(food,grocery,cleaning,supply,item,resource,necessity,essential)]":{
            'score':3.0,
            '[!#SET($shopping_challenge=True) "I cannot believe how empty the grocery store shelves are. Everything seems to be missing, '
            'but I hope you are able to find what you need."]': 'exit'
        },

        "[#EXP(coronavirus)]":{
            'score':3.0,
            '"Oh, yes. The coronavirus outbreak that is happening right now has a dramatic impact on everyone\'s '
            'lives at this point. "': 'exit'
        },

        "[{#LEM(fart,poop,shit,crap,piss,pee,urinate,tinkle),pooped,[#LEM(take),dump]}]":{
            '"Okay, that is kind of gross for you to share with me, but good for you, I guess? '
            'I really would rather talk about something else, so we are moving on now. "': 'exit'
        },

        "{"
        "[#LEM(fuck)],"
        "[#LEM(jerk,suck,masturbate,eat),{#EXP(genitalia),off,me,myself,#ONT(related_person)}],"
        "[#LEM(have,do),#EXP(sex)],"
        "[{porn,xrated,x rated}],"
        "[#LEM(make),{love,sex}]"
        "}":{
            '"You seem to be sharing some pretty personal details of your life. I am not sure this is the best time or '
            'place for that, and I do not know anything about those activities. So, we should move on to a '
            'more appropriate topic. "': 'exit'
        }

    }
}

exit = {
    'state': 'exit',

    '#GCOM(hobby) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user'
}

hobby.load_transitions(system)
hobby.load_transitions(exit)
hobby.load_global_nlu(user)


if __name__ == '__main__':
    hobby.run(debugging=True)