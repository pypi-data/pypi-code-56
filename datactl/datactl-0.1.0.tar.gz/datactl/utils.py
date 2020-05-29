import ast
import copy
import datetime
import json
import os
import secrets
import sys
import random
import urllib.parse
import uuid
from pathlib import Path

import pendulum
import yaml
from termcolor import colored, cprint
from terminaltables import AsciiTable

quote = urllib.parse.quote_plus


def require_dir(path):
    if not Path.exists(Path(path)):
        os.makedirs(path, exist_ok=True)
    return path


def require_file(path):
    require_dir(path.parent)
    Path.touch(path)
    return path


def get_value(value, key, from_config, config_obj, ttype=None, default=None):
    if value is not None:
        res = value
    elif from_config:
        res = config_obj.get(from_config, key)
    else:
        res = None
    if res is not None and ttype:
        if ttype == bool:
            res = str_to_bool(res)
        else:
            res = ttype(res)
    if res is None and default is not None:
        res = default
    return res


def to_list_of_dict(data):
    table_data = []
    for row in data:
        try:
            row = ast.literal_eval(row)
        except:
            pass
        if not isinstance(row, dict):
            row = dict(row)
        if '_id' in row:
            row['_id'] = str(row['_id'])
        table_data.append(row)
    return table_data


def to_dict(value):
    if not isinstance(value, dict):
        return ast.literal_eval(value)
    return value


def dry_run(data, obj):
    if obj._dry_run:
        show_data(data, obj)
        sys.exit(0)


def prepare_data(msg, obj):
    msgs = []
    for i in range(1, obj._size+1):
        if msg:
            msg_copy = str_to_dict(msg)
        else:
            msg_copy = dict()
        if obj._template:
            msg_copy.update(str_to_dict(obj._template))
        if obj._template_file:
            msg_copy.update(str_to_dict(Path(obj._template_file).read_text()))
        if obj._data:
            msg_copy.update(str_to_dict('dict({})'.format(obj._data), idx=i))
        if obj._metadata:
            msg_copy.update(dict(
                meta_date=now_str(utc=False),
                meta_date_utc=now_str(utc=True),
                meta_uid=str(uuid.uuid4()),
                meta_id=i,
            ))
        msgs.append(copy.deepcopy(msg_copy))
    return msgs


def confirm(obj):
    #pylint: disable=R1705
    if obj._yes:
        return True
    while True:
        res = input('do you want to continue ? [y/n]: ')
        res_norm = res.lower().strip()[:3]
        if res_norm in ('yes', 'y', 'ye'):
            return True
        elif res_norm in ('no', 'n'):
            return False


def abort(msg='Aborted !'):
    cprint(colored(msg, color='red'))
    sys.exit(0)


def now_str(utc=False):
    if utc:
        return datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


def show_data(data, obj):
    data = clean_data(data, obj)
    if obj._output == 'table':
        show_table(data)
    elif obj._output == 'json':
        show_json(data)
    elif obj._output == 'yaml':
        show_yaml(data)
    else:
        abort('the output [%s] is not implemented' % obj._output)


def clean_data(data, obj):
    if obj._columns:
        columns = obj._columns
        if isinstance(obj._columns, (tuple, list)):
            columns = ','.join(columns)
        columns = columns.strip().replace(' ', '').replace(':', ',').split(',')
        if columns:
            new_data = []
            for line in data:
                new_line = {}
                to_show = set(line.keys()).intersection(columns)
                for col in to_show:
                    new_line[col] = line[col]
                new_data.append(new_line)
            return new_data
    if obj._hide:
        columns = obj._hide
        if isinstance(columns, (tuple, list)):
            columns = ','.join(columns)
        columns = columns.strip().replace(' ', '').replace(':', ',').split(',')
        if columns:
            for line in data:
                for col in columns:
                    line.pop(col, None)
    return data


def show_table(data):
    table_data = []
    if isinstance(data, (dict,)):
        data = [data]
    if data:
        keys = set()
        for row in data:
            [keys.add(x) for x in row.keys()]  # pylint: disable=W0106
        table_data.append(keys)
        for row in data:
            table_data.append([row.get(k, '') for k in keys])
    print(AsciiTable(table_data).table)


def show_yaml(data):
    print(yaml.dump(data, default_flow_style=False))


def show_json(data):
    json_formatted_str = json.dumps(data, indent=2)
    print(json_formatted_str)


def str_to_bool(text):
    if isinstance(text, (str, bytes)):
        if text.strip().lower() in ('yes', 'ye', 'y', 'true', 1):
            return True
        return False
    return bool(text)


def str_to_dict(s, idx=1):
    def _Date(start, stop):
        if not stop:
            stop = start
        start = pendulum.parse(start).timestamp()
        stop = pendulum.parse(stop).timestamp()
        return pendulum.from_timestamp(round(random.uniform(start, stop)))

    def Date(start, stop=False):
        return _Date(start, stop).to_date_string()

    def DateTime(start, stop=False):
        return _Date(start, stop).to_datetime_string()

    def RandInt(start, stop):
        return int(round(random.uniform(start, stop)))

    def RandFloat(start, stop):
        return random.uniform(start, stop)

    def Choice(*args):
        return random.choice(args)

    def Hash(size=4):
        return secrets.token_hex(nbytes=size)
    #pylint: disable=W0123
    context = dict(
        Date=Date,
        DateTime=DateTime,
        RandInt=RandInt,
        RandFloat=RandFloat,
        Hash=Hash,
        Choice=Choice,
        ID=lambda: idx,
        UUID=lambda: str(uuid.uuid4()),
        NOW=lambda s=False: pendulum.now().to_datetime_string(
        ) if s else pendulum.now().to_date_string(),
    )
    if isinstance(s, dict):
        context.update(s)
        for k, v in s.items():
            try:
                s[k] = eval(v, context)
            except:
                pass
        return s
    return eval(s, context)


if __name__ == "__main__":
    pass
