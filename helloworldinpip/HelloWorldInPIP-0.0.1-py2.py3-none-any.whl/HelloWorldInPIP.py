# coding=utf-8

# <editor-folder desc="导入包">

# 时间
import time
import datetime

# </editor-folder>

# <editor-folder desc="类">
# </editor-folder>

# <editor-folder desc="方法">

def print_string(data_output):

    print("传入的字符串是：【" + str(data_output) + "】")

def print_date(action_type):

    if action_type == "当前时间" \
        or action_type == "today":
        print("当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    if "往前" in action_type:
        how_much = str(action_type).split('前')[1].split('天')[0]
        today = datetime.date.today()
        oneday = datetime.timedelta(days=int(how_much))
        finally_day = today - oneday

        print(action_type + "：" + str(finally_day))

    elif "往后" in action_type:
        how_much = str(action_type).split('后')[1].split('天')[0]
        today = datetime.date.today()
        oneday = datetime.timedelta(days=int(how_much))
        finally_day = today + oneday

        print(action_type + "：" + str(finally_day))

    # </editor-folder>