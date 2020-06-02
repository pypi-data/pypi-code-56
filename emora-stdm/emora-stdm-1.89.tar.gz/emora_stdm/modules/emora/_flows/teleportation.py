### (SYSTEM) TALK ABOUT TELEPORTATION
share_teleport_fun = ['"It would be so cool for teleportation to be real. It would take a lot less time for people to travel around."',
                      '"I am really excited about the idea of teleportation for people. You would be able to just instantly travel from place to place."']
df.add_system_transition(State.SCIFI, State.SHARE_TELEPORT_FUN, share_teleport_fun)
df.update_state_settings(State.SHARE_TELEPORT_FUN, system_multi_hop=True)

ask_teleport_opi = ['"What do you think about the possibility of teleportation?"',
                    '"What is your opinion on teleportation?"']
df.add_system_transition(State.SHARE_TELEPORT_FUN, State.ASK_TELEPORT_OPI, ask_teleport_opi)

### (USER) DOESNT KNOW TELEPORTATION
teleport_unknown = '{' \
               '[{[!{dont,do not}, know],not sure,unsure,uncertain}, what, {that,teleportation,it,teleport,you said}, {is,mean,means}],' \
               '[what,is,{that,teleportation,it,teleport,you said}],' \
               '[what,does,{that,teleportation,it,teleport,you said},mean]' \
               '}'
df.add_user_transition(State.ASK_TELEPORT_OPI, State.REC_TELEPORT_UNKNOWN, teleport_unknown,score=0.9)
df.add_system_transition(State.REC_TELEPORT_UNKNOWN, State.ASK_TELEPORT_OPI,
                                '"It seems like you are not sure what teleportation is. Teleportation is the process '
                                'of moving an object from one location to another instantaneously and it is commonly '
                                'referenced in science fiction. So, what do you think about that idea?"')

### (USER) SHARE OPINION ON TELEPORTATION
teleport_fun = '{' \
               '[!#ONT_NEG(ont_negation) [{agree, [! think {so,that} too]}]],' \
               '[!#ONT_NEG(ont_negation) [{fun,exciting,excited,[looking,forward],good,great,cool,awesome,neat,amazing,wonderful,fantastic,sweet}]],' \
               '[!#ONT_NEG(ont_negation) [i,{like,into},{it,teleportation,teleport}]]' \
               '[!#ONT(ont_negation) [{scary,scared,terrifying,terrified,horrified,horrifying,fear,fearful,bad,horrible,terrible,danger,dangerous,frightening,frightened,frightens}]]' \
               '}'
df.add_user_transition(State.ASK_TELEPORT_OPI, State.REC_TELEPORT_FUN, teleport_fun)
teleport_scary = '{' \
               '[!#ONT(ont_negation) [{agree, [! think {so,that} too]}]],' \
               '[!#ONT_NEG(ont_negation) [{scary,scared,scares,terrifying,terrified,terrifies,horrified,horrifying,horrifies,fear,fearful,bad,horrible,terrible,danger,dangerous,frightening,frightened,frightens,worry,worrying,worried,pain,painful,suffering,death,misery,die,dying}]],' \
               '[!#ONT(ont_negation) [{fun,exciting,good,great,cool,awesome,neat,amazing,wonderful,fantastic,sweet}]],' \
               '[!#ONT(ont_negation) [i,{like,into},{it,teleportation,teleport}]]' \
               '}'
df.add_user_transition(State.ASK_TELEPORT_OPI, State.REC_TELEPORT_SCARY, teleport_scary)
teleport_unlikely = '[{' \
               'unlikely,impossible,' \
               '[{dont,not,never},{happen,happening,real,likely}]' \
               '}]'
df.add_user_transition(State.ASK_TELEPORT_OPI, State.REC_TELEPORT_UNLIKELY, teleport_unlikely)
uncertain_expression_nlu = ["[#ONT(uncertain_expression)]"]
df.add_user_transition(State.ASK_TELEPORT_OPI, State.REC_TELEPORT_UNSURE, uncertain_expression_nlu)
df.set_error_successor(State.ASK_TELEPORT_OPI, State.HARDEST_PART)

### (SYSTEM) RESPOND TO USER FUN
df.add_system_transition(State.REC_TELEPORT_FUN, State.FIRST_PERSON,
                         ['[!#GATE(first_person:None) "Yeah, it would be pretty awesome."]', '"Cool, you like teleportation too? I am glad we agree!"'])
df.update_state_settings(State.FIRST_PERSON, system_multi_hop=True)
df.add_system_transition(State.FIRST_PERSON, State.REC_FIRST_PERSON, '[! "Would you be one of the first people to try teleportation?" #SetTrue(first_person)]')
yes_first_person = "[! #ONT_NEG(ont_negation) [{#EXP(yes), [i, would], [i, think, so]}]]"
df.add_user_transition(State.REC_FIRST_PERSON, State.YES_FIRST_PERSON, yes_first_person)
no_first_person = "[{#EXP(no), [i, would, not], [i, {dont,do not}, think, so]}]"
df.add_user_transition(State.REC_FIRST_PERSON, State.NO_FIRST_PERSON, no_first_person)
df.set_error_successor(State.REC_FIRST_PERSON, State.MIS_FIRST_PERSON)

df.add_system_transition(State.YES_FIRST_PERSON, State.TRANS, '"You would volunteer so early? That is so courageous! I don\'t think I could gather the courage to do that."')
df.add_system_transition(State.NO_FIRST_PERSON, State.TRANS, '"Yeah, I definitely need other people to test it out first, too. Safety is important, for sure."')
df.add_system_transition(State.MIS_FIRST_PERSON, State.TRANS, '"I see. That is an interesting point. Personally, I don\'t think I could be one of the first people to try it out."')

### (SYSTEM) RESPOND TO USER SCARED
df.add_system_transition(State.REC_TELEPORT_SCARY, State.TRANSPORT_FAIL,
                         ['[!#GATE(transport_fail:None) "Oh, that is true. It could be kind of scary, for sure."]', '"You bring up a good point. Depending, it could be a bit dangerous."'])
df.update_state_settings(State.TRANSPORT_FAIL, system_multi_hop=True)
df.add_system_transition(State.TRANSPORT_FAIL, State.REC_TRANSPORT_FAIL_OPI, '[! "I think the scariest part would be not making it to the destination in one piece. Are you scared of that too?" #SetTrue(transport_fail)]')
df.add_user_transition(State.REC_TRANSPORT_FAIL_OPI, State.YES_TRANSPORT_FAIL, '{#EXP(yes), [! #ONT_NEG(ont_negation) [i, am]]}')
df.add_user_transition(State.REC_TRANSPORT_FAIL_OPI, State.NO_TRANSPORT_FAIL, '{#EXP(no), [i am #ONT(ont_negation)]}')
df.set_error_successor(State.REC_TRANSPORT_FAIL_OPI, State.MIS_TRANSPORT_FAIL)

df.add_system_transition(State.YES_TRANSPORT_FAIL, State.TRANS, '"Oh boy. It makes me shake just thinking about it!"')
df.add_system_transition(State.NO_TRANSPORT_FAIL, State.TRANS, '"Really? You are not scared of that? Maybe you know something I don\'t."')
df.add_system_transition(State.MIS_TRANSPORT_FAIL, State.TRANS, '"That is a good point, for sure. I never thought of it like that."')

### (SYSTEM) RESPOND TO USER UNLIKELY
df.add_system_transition(State.REC_TELEPORT_UNLIKELY, State.HARDEST_PART,
                         ['[!#GATE(hardest_part:None) "We will just have to wait and see, I guess."]', '"Yeah, at this point, it is just fiction, after all."'])
df.add_system_transition(State.HARDEST_PART, State.REC_HARDEST_PART, '[! "I am curious to know. What do you think is the hardest part of actually making a teleportation device?" #SetTrue(hardest_part)]')
df.update_state_settings(State.HARDEST_PART, system_multi_hop=True)
construct_nlu = "{" \
                "[taking, apart], [putting, together], [{deconstruct,deconstructing,construct,constructing,reconstruct,reconstructing,build,building,make,making,form,forming,break,breaking}], " \
                "[first, {one,thing}]" \
                "}"
df.add_user_transition(State.REC_HARDEST_PART, State.HARDEST_CONSTRUCTION, construct_nlu)
transport_nlu = "{" \
                "[{transport,transporting,transportation,transfer,transferring,send,sending,mechanics}], " \
                "[{second,last,final}, {one,thing}]" \
                "}"
df.add_user_transition(State.REC_HARDEST_PART, State.HARDEST_TRANSPORTATION, transport_nlu)
df.set_error_successor(State.REC_HARDEST_PART, State.HARDEST_OTHER)

df.add_system_transition(State.HARDEST_CONSTRUCTION, State.TRANS, '"Yeah, I think the item reconstruction is the hardest for sure. But I am not a scientist, so I could be wrong."')
df.add_system_transition(State.HARDEST_TRANSPORTATION, State.TRANS, '"Yeah, I\'m not a scientist, so I have no idea how items can be transported immediately from one location to another."')
df.add_system_transition(State.HARDEST_OTHER, State.TRANS, '"Yeah, that is true. There are probably many difficult pieces in the puzzle of teleportation, but we can leave that up to the scientists."')

### (SYSTEM) PICK NEXT QUESTION FROM THOSE NOT ASKED BEFORE
df.update_state_settings(State.TRANS, system_multi_hop=True, memory=0)
df.add_system_transition(State.TRANS, State.HARDEST_PART, "[! #GATE(hardest_part:None) .]", score=0.8)
df.add_system_transition(State.TRANS, State.FIRST_PERSON, "[! #GATE(first_person:None) .]", score=0.9)
df.add_system_transition(State.TRANS, State.TRANSPORT_FAIL, "[! #GATE(transport_fail:None) .]", score=1.0)
df.add_system_transition(State.TRANS, State.FINISH_TELEPORT, "", score=0.0)

df.update_state_settings(State.FINISH_TELEPORT, system_multi_hop=True)
df.add_system_transition(State.FINISH_TELEPORT, State.TRANSITION_OUT, '" "')
#df.add_system_transition(State.FINISH_TELEPORT, State.TRANSITION_OUT, '"I have really enjoyed talking about this invention in science fiction with you. I am interested in learning more about your opinions on other things too!"')

### (SYSTEM) RESPOND TO USER UNSURE
df.add_system_transition(State.REC_TELEPORT_UNSURE, State.TRANS,
                         ['"Real teleportation is still a bit out of reach, so it is hard to predict how you will feel about it."', '"I get it. It is hard to have an opinion on something we do not know much about at this point."'])


























from _globals import PATHDIR
from emora_stdm import DialogueFlow


teleportation = DialogueFlow('_local_start')
teleportation.knowledge_base().load_json_file(PATHDIR.replace('__***__', '_common.json'))
teleportation.add_system_transition('_local_start', 'start', '')

system = {
    'state': 'start',
    'enter': '#GATE #GCOM(teleportation) #GOAL(teleportation)',

    '#DEFAULT': {
        'state': 'default_start',
        'hop': 'True',

        '`Wait, so what do you think about the possibility of teleportation?`':
            'teleportation_q'
    },
    '"What do you think about the possibility of teleportation?"'
    '#GSRET(default_start)': {
        'state': 'teleportation_q',

        '{'
        '[#NOT(not),#ONT(_positive adj)]'
        '}':{
            'state': 'teleportation_good',

            '':{

            }
        }
    }
}

exit = {
    'state': 'exit',

    '#GCOM(teleportation) #GRET': {
        'score': 0.9,
        'state': 'SYSTEM:root'
    }
}

user = {
    'state': 'user',

    '{' 
    '[{[!{dont,do not}, know],not sure,unsure,uncertain}, what, {that,teleportation,it,teleport,you said}, {is,mean,means}],' 
    '[what,is,{that,teleportation,it,teleport,you said}],'
    '[what,does,{that,teleportation,it,teleport,you said},mean]'
    '}': {
        'state': 'what_is_teleportation',

        'Teleportation is the process of moving an object from one location to another instantaneously and it is commonly '
        'referenced in science fiction.': {
            'state': 'explain_teleportation',

            '#UNX': {'#GRET': 'exit', 'state': 'teleportation_unx'}
        }
    }
}

teleportation.load_transitions(system)
teleportation.load_transitions(exit)
teleportation.load_global_nlu(user)


if __name__ == '__main__':
    teleportation.run(debugging=True)






