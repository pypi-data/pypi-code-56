from collections import defaultdict
from datetime import datetime

from .items import (
    get_collection,
    get_item,
    get_item_by_code,
    items_for_collection,
    parse_data,
)
from .models import Settings
from .sheet_transform import get_col_item_needs, get_no_hide_collections, get_rows


def get_important(rows):
    imp_items = defaultdict(set)

    for col_name, items in get_col_item_needs(rows).items():
        for item_name in items:
            of_import = not item_name.startswith('!')
            item_name = item_name.strip('!')
            item = get_item(item_name, col_name)
            print(f'{col_name:>30} - {item_name:>30} --> {item.name}')
            imp_items[of_import].add(item)

    return imp_items[True], imp_items[False]


def remove_no_hide_cols(unimportant, rows):
    no_hide_col_names = get_no_hide_collections(rows)
    no_hide_cols = [get_collection(name) for name in no_hide_col_names]

    return {it for it in unimportant if it.collection not in no_hide_cols}


def get_settings(sheet_name=None):
    _, items = parse_data()
    sheet_conf = {'sheet_name': sheet_name} if sheet_name else {}
    rows = get_rows(**sheet_conf)

    important, unimportant = get_important(rows)

    # always mark weekly items as important
    weekly_items = items_for_collection('Weekly', items)
    for item in weekly_items:
        item_in_orig_coll = get_item_by_code(item.code, items)
        important.add(item_in_orig_coll)

    unimportant |= items - important

    unimportant = remove_no_hide_cols(unimportant, rows)

    return Settings(important_items=important, unimportant_items=unimportant)


def get_export_filename():
    now = datetime.now()
    return now.strftime('%Y-%m-%d_%H-%M-%S.json')


def write_export(export_path):
    path = export_path / get_export_filename()

    s = get_settings()
    path.write_text(s.as_json())

    print(f'export written to {path}')
