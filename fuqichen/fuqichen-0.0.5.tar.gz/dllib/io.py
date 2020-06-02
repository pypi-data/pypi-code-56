import csv
import json
import pickle


def read_csvfile(filename, keys=set(), label_only=False):
    out = []
    with open(filename, mode='r') as f:
        reader = csv.reader(f)
        fieldnames = next(reader)
        if label_only:
            return fieldnames
        if not keys:
            keys = set(fieldnames)
        csv_reader = csv.DictReader(f, fieldnames=fieldnames)
        for idx, row in enumerate(tqdm(csv_reader, ncols=60, desc='loading {}'.format(filename))):
            d = {}
            for k in keys:
                d[k] = row[k]
            out.append(d)
    return out

def save_csv(filename, obj, header=''):
    with open(filename, "wt") as f:
        writer = csv.writer(f, delimiter=",")
        if header:
            writer.writerow(header)  # write header
        writer.writerows(obj)


def read_pickle(filename):
    with open(filename, 'rb') as filehandle:
        obj = pickle.load(filehandle)
    return obj


def save_pickle(filename, obj):
    with open(filename, 'wb') as filehandle:
        pickle.dump(obj, filehandle)


def read_json(filename):
    obj = json.load(filename)
    return obj


def save_json(filename, obj):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)
