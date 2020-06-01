"""
REAM: REAM Ain't Markdown
~~~~~~~~~~~~~~~~~~~~~~~~~

This file is part of the ream package

:copyright: Copyright 2020 by Chih-Ming Louis Lee
:license: MIT, see LICENSE for details

"""
import sys
import os
import re
import json
import yaml
import pandas as pd
from ream.transformer import Ream2Dict
from ream.grammar import REAM_RULE

def ream2dict(input_raw, output_file=None, debug=False, no_comment=False):
    """ream to json"""

    if no_comment:
        Ream2Dict.no_comment = True
    else:
        Ream2Dict.no_comment = False

    input_tree = REAM_RULE.parse(input_raw)
    output_raw = Ream2Dict().transform(input_tree)

    if debug:
        print(input_tree)
        print("====================")
        print(input_tree.pretty())
        print("====================")
        print(output_raw)
        print("====================")

    if output_file is None:
        return output_raw
    else:
        with open(output_file, 'w') as file:
            json.dump(output_raw, file)
        print(json.dumps(output_raw, indent=4))
        return None



def ream2list(input_raw):

    data = ream2dict(input_raw, no_comment=True)

    ## extract metadata
    #try:
    #    metadata = data['__METADATA__'][0]
    #except KeyError:
    #    print("metadata not found")

    #data.pop('__METADATA__')


    #if 'see' in metadata:
    #    metadata_path = metadata['see'][1:-1]
    #    metadata_raw = ream2dict(metadata_path, no_comment=True)
    #    metadata = metadata_raw['__METADATA__'][0]

    #if '__CSV__' not in metadata:
    #    print("csv format not defined")
    #    #sys.exit()

    ## extract csv config
    #try:
    #    row = metadata['__CSV__'][0]['row']
    #    col = metadata['__CSV__'][0]['col']
    #except KeyError:
    #    print("Check your csv config")
    #    #sys.exit()

    ## extract format
    #try:
    #    form = metadata['__FORMAT__'][0]
    #except KeyError:
    #    print("Missing info for format")
    #    #sys.exit()

    ## clean row and col names
    #row = row[1:-1]
    #col = [item[1:-1] for item in col]


    def convert_list(list_outer):
        output = []
        for entry in list_outer:
            output_inner = []
            for value in entry.values():
                if isinstance(value, str):
                    output_inner.append(value)
                else:
                #if isinstance(value, list):
                    output_inner.append(convert_list(value))
            output.append(output_inner)
        return output

    def convert_dictionary(dictionary):
        output = []
        for value in dictionary.values():
            if isinstance(value, str):
                output.append(value)
            else:
            #if isinstance(value, list):
                output += convert_list(value)
        return output


    def flatten_list_inner(list_inner):
        if isinstance(list_inner[0], str) and isinstance(list_inner[-1], list):
            parent = list_inner[:-1]
            children = list_inner[-1]
            output_inner = []
            for child in children:
                child = flatten_list_inner(child)
                if isinstance(child[0], list):
                    for entry in child:
                        output_inner.append(parent + entry)
                else:
                    output_inner.append(parent + child)
            return output_inner
        else:
            return list_inner


    def flatten_list_outer(list_outer):
        output_outer = []
        for item in list_outer:
            output_outer.append(flatten_list_inner(item))
        if isinstance(output_outer[0][0], list):
            return [level_2 for level_1 in output_outer for level_2 in level_1]
        return output_outer


    return flatten_list_outer(convert_dictionary(data))

def ream2csv(input_raw, output_file):

    list_raw = ream2list(input_raw)

    with open(output_file, 'w') as file:
        colname = ",".join([str(x) for x in range(len(list_raw[0]))])
        file.write(colname)
        file.write('\n')
        for entry in list_raw:
            file.write(",".join(entry))
            file.write('\n')

def ream2df(data):
    return pd.DataFrame(ream2list(data))

def main(input_raw, output_file, debug, no_comment):
    """
    main function for decoding ream file
    """

    output_ext = output_file.split('.')[-1]

    # choose conversion function
    if output_ext in ['json']:
        ream2dict(input_raw, output_file, debug, no_comment)
    elif output_ext in ['csv']:
        ream2csv(input_raw, output_file)
    else:
        print("Output file formet not supported")
    print("Complete")
