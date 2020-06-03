from __future__ import print_function, unicode_literals
from pprint import pprint
from tinydb import TinyDB, where, Query
import sys
import os
import uuid # creating unique id's for storage
from pathlib import Path # for finding user's home
from os.path import join as join_path
from datetime import datetime,timedelta
from prompt_toolkit import prompt,print_formatted_text
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.formatted_text import FormattedText
from reflect.menus import *



def today():
    return datetime.now().strftime("%Y%m%d")

def clear_screen():
    clear()

def get_pos(questions, question_text ):
    for i,q in enumerate(questions):
        if question_text==q["text"]:
            return i

def do_reflection(time, data_base):
    # load questions from database
    Questions = Query()
    questions = get_questions(time, data_base)
    # TODO check for empty questions
    if len(questions)==0:
        clear_screen()
        print("No questions for %s reflection. Add some questions.\n"%time )
        return

    #load answers for today if they are there
    Answers = Query()
    old_answers = data_base.search( (Answers.time == time) & (Answers.date==today()) & (Answers.type=="reflection") )
    old_answers = (old_answers[0] if len(old_answers)>0 else {})

    answers = {}
    answers["time"]=time
    answers["type"]="reflection"
    answers["date"]=today()
    # store answers for today in database
    ref_qs = []
    for i, q in enumerate(questions):
        default = old_answers[q["id"]] if q["id"] in old_answers else ""
        new_answer = prompt( [('class:key',q["text"].replace("?","")+"?"),('class:default_answer'," <%s>: "%default) ], style=style)
        if len(new_answer)>0:
            answers[q["id"]] = new_answer
        else:
            answers[q["id"]] = default

        if len(old_answers)==0 and i==0:
            data_base.insert(answers)
        else:
            data_base.update(answers, (Answers.time == time) & (Answers.date==today()) & (Answers.type=="reflection") )

    clear()
    print("%s-reflection stored.\n"%time)

def get_questions(time, data_base):
    Questions = Query()
    questions = data_base.search( Questions.time == time)
    if len(questions)==0:
        data_base.insert({'questions':questions, "time":time})
        questions=[]
    else:
        questions=[q for q in questions[0]["questions"] if not q["deleted"]]

    # todo add sort order
    return questions


def add_questions(time, data_base):
    # load existing questions
    action=""
    while True:
        clear_screen()
        # get old questions
        questions=get_questions(time, data_base)
        # get new question
        menu = []
        menu.append( ('class:title','Existing questions \n' ) )
        menu.append( ('class:separator',"="*20+"\n\n") )
        for i,q in enumerate(questions):
            menu.append( ('class:key','(%s) '%(i+1) )  )
            menu.append( ('class:menu_item',' %s \n'%q["text"] )  )

        menu.append( ('class:input',"Question to add: > " ) )

        new_question_text=prompt( menu , style=style)
        if len(new_question_text)==0:
            clear_screen()
            print("Empty text, no question added.")
            return

        if not new_question_text[-1]=="?":
            new_question_text=new_question_text+"?"

        for q in questions:
            if new_question_text==q["text"]:
                clear_screen()
                print("Duplicate question '%s' not added."%new_question_text)
                return

        new_question={"text":new_question_text, "id":str(uuid.uuid4()), "deleted":False }
        questions += [ new_question ]
        #store new question
        Questions=Query()
        data_base.update({'questions':questions}, Questions.time == time)
        clear_screen()
        print("Question successfully added.\n")
        # prompt if you want to add more questions?

        items = {
            "title":{"text":"What do you want to do?"},
            "<any>":{"text":"Add further questions", "handler": quit},
            "b":{"text":"Back", "handler": quit },
        }
        key_pressed = key_press_menu(items)
        if key_pressed=="b" or key_pressed=="escape":
            clear_screen()
            return

def delete_questions(time, data_base):
    # load existing questions
    action=""
    while True:
        clear_screen()
        # get old questions
        questions=get_questions(time, data_base)
        if (len(questions)==0):
            clear_screen()
            print("No questions for %s stored."%time )
            return
        # get new question
        delete_action=menu_from_questions(questions, "Which question do you want to delete?")

        if delete_action == "escape" or delete_action=="q":
            clear_screen()
            print("Aborted deleting.\n")
            return

        # validate user input
        if not delete_action.isnumeric() or int(delete_action)-1  not in list(range(len(questions))):
            clear_screen()
            print("'%s' is an invalid input, aborting.\n"%delete_action)
            return

        # delete data
        questions[int(delete_action)-1]["deleted"]=True


        Questions = Query()
        data_base.update({'questions':questions}, Questions.time == time)
        clear_screen()
        print("Question for %s reflection deleted .\n"%time)

def change_order(time, data_base):
    # load existing questions
    action=""
    clear_screen()
    while True:

        # get old questions
        questions=get_questions(time, data_base)
        if (len(questions)<=1):
            clear_screen()
            print("No or too few questions for %s reflection stored. Add more reflections to change the order."%time )
            return
        # get new question

        move_from=menu_from_questions(questions, "Which question do you want to move?")

        if move_from == "q" or move_from == "escape":
            clear_screen()
            print("Aborted order change.\n")
            return

        if not move_from.isnumeric() or int(move_from)-1 not in list(range(len(questions))):
            clear_screen()
            print("'%s' is an invalid input, aborting.\n"%move_from)
            return

        # get new question

        loop_text = formatted_questions(questions," Which question do you want to move?")
        sel_pos = -1
        for i, l in enumerate(loop_text):
            if l[1]=="(%s) "%move_from:
                sel_pos=i
                break
        if sel_pos>-1:
            loop_text[sel_pos] = ('class:current_key', loop_text[sel_pos][1])
            loop_text[sel_pos+1] = ('class:current_key', loop_text[sel_pos+1][1])

        clear_screen()
        move_to=menu_from_questions(questions, "To which position do you want to move it to?", loop_text )

        if move_to == "q" or move_to == "escape":
            clear_screen()
            print("Aborted order change.\n")
            return

        # move question
        if not move_to.isnumeric() or int(move_to)-1  not in list(range(len(questions))):
            clear_screen()
            print("'%s' is an invalid input, aborting.\n"%move_to)
            return

        # validate user input
        questions.insert(int(move_to)-1, questions.pop(int(move_from)-1 ))

        # update in database
        Questions=Query()
        data_base.update({'questions':questions}, Questions.time == time)
        clear_screen()
        print("Question moved.\n")

def change_password(data_base): ##TODO  Move to encrypted file storage
    from os.path import join as join_path
    action=""

    new_encryption_key1 = prompt( [('class:key','New Password? ' )], is_password=True, style=style)
    new_encryption_key2 = prompt( [('class:key','Repeat New Password? ' )], is_password=True, style=style)

    if not (new_encryption_key1==new_encryption_key2):
        print("New passwords don't match, aborting.")
        return

    if data_base.storage.change_encryption_key(new_encryption_key1):
        print("Password successfully changed\n")
    else:
        print("Error, password was not changed.\n")

def modify_questions(time, data_base):
    # load existing questions
    action=""
    clear_screen()
    while True:
        # get old questions
        Questions = Query()
        questions = get_questions(time, data_base)
        if (len(questions)==0):
            clear_screen()
            print("No questions for %s reflection stored."%time )
            return

        # get new question
        mod_action=menu_from_questions(questions, "Which question do you want to modify?")

        if mod_action == "q" or mod_action=="escape":
            clear_screen()
            print("Aborted modification.\n")
            return
        if not mod_action.isnumeric() or int(mod_action)-1  not in list(range(len(questions))):
            clear_screen()
            print("'%s' is an invalid input, aborting.\n"%delete_action)
            continue
        question_id = int(mod_action)-1


        # modify data
        # get new question
        menu = []
        menu.append( ('class:title','New question text? \n' ) )
        menu.append( ('class:menu_item','<%s> \n'%questions[question_id]["text"] ) )
        menu.append( ('class:input',"> " ) )
        modified_question_text=prompt(menu, style=style)

        if len(modified_question_text)==0:
            clear_screen()
            print("Empty text, question not modified. If you want to delete a question, use the delete menu.")
            continue

        if not modified_question_text[-1]=="?":
            modified_question_text=modified_question_text+"?"

        for q in questions:
            if modified_question_text==q["text"]:
                clear_screen()
                print("Duplicate question, question not changed."%modified_question_text)
                continue

        questions[question_id]["text"]=modified_question_text
        data_base.update({'questions':questions}, Questions.time == time)
        clear_screen()
        #TODO proper messageb
        print("Question for %s reflection has been updated.\n"%time)

"""
    Exports all answers to a text file
"""
def export(data_base):
    outfile = join_path(join_path(str(Path.home()),"exported_reflections_%s.txt"%today()) )
    questions = {}
    questions["Morning"] = get_questions("Morning", data_base)
    questions["Evening"] = get_questions("Evening", data_base)

    # get all answer
    Answers = Query()
    answers = data_base.search( Answers.type=="reflection")
    dates = sorted(set([a['date'] for a in answers] ))

    # create a dictionary [date][time] answers
    answers_by_date = {}
    for a in answers:
        if not a["date"] in answers_by_date:
            answers_by_date[a["date"]]={}
        answers_by_date[a["date"]][a["time"]]=a


    with open(outfile, "w+") as f:
        for d  in dates:
            if not d in answers_by_date:
                continue

            f.write(d[0:4]+"-"+d[4:6]+"-"+d[6:]+"\n")
            f.write("==========\n")

            for t in ["Morning","Evening"]:
                if t in answers_by_date[d]:
                    f.write("%s:\n"%(t))
                    for q in questions[t]:
                        if q["id"] in answers_by_date[d][t]:
                            f.write("\t")
                            f.write(q["text"]+"\t")
                            f.write(answers_by_date[d][t][q["id"]]+"\n")
                    f.write("\n")

            f.write("\n\n")


    print("Your reflections were exported to '%s'\n"%outfile)
    pass

def day_string(date,data_base):
    # load questions from database
    morning_questions = get_questions("Morning", data_base)
    evening_questions = get_questions("Evening", data_base)
    questions = {
        "Morning":morning_questions,
        "Evening":evening_questions
    }

    #load answers for date if they are there
    Answers = Query()
    morning_answers = data_base.search( (Answers.time == "Morning") & (Answers.date==date) & (Answers.type=="reflection") )
    morning_answers = (morning_answers[0] if len(morning_answers)>0 else {})

    evening_answers = data_base.search( (Answers.time == "Evening") & (Answers.date==date) & (Answers.type=="reflection") )
    evening_answers = (evening_answers[0] if len(evening_answers)>0 else {})
    answers_by_date = {
        "Morning":morning_answers,
        "Evening":evening_answers
    }

    formatted_answers  = []
    formatted_answers.append( ('class:title', date[0:4]+"-"+date[4:6]+"-"+date[6:]+"\n") )
    formatted_answers.append( ('class:separator', "="*20+"\n\n") )

    for t in ["Morning","Evening"]:
        if t in answers_by_date:
            formatted_answers.append(  ('class:title',"%s:\n"%(t)) )
            for q in questions[t]:
                if q["id"] in answers_by_date[t]:
                    formatted_answers.append( ('class:key',"\t%s:"%q["text"]) )
                    formatted_answers.append( ('class:menu_item',"\t%s\n"%answers_by_date[t][q["id"]]) )
            formatted_answers.append(  ('class:title',"\n") )

    formatted_answers.append(  ('class:title',"\n") )
    return formatted_answers

def change_date(current_date, offset_in_days):

    offset = timedelta(days=offset_in_days)
    current_date = datetime.strptime(current_date,"%Y%m%d")
    current_date = current_date + offset
    return current_date.strftime("%Y%m%d")

def browse(current_date, data_base ):

    while True:

        # show menu
        action = browse_menu(day_string(current_date, data_base ))
        clear()

        if action=="b":
            return
        elif action=="p" or action =="Keys.Right":
            current_date = change_date(current_date, -1)
            continue
        elif action=="n" or action =="Keys.Left":
            current_date = change_date(current_date, 1)
            continue
        elif action == "g":
            browse_date = prompt( [('class:key','Which day do you want to display (YYYYMMDD)? ' )], style=style)
            try:
                datetime.strptime(browse_date,"%Y%m%d") #check if formatted correctly
                current_date = browse_date
            except:
                print("Invalid date, use format YYYYMMDD, e.g. 20200420")
            continue
