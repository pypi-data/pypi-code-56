import configparser
import json
import os

from sharepoint_too import SharePointSession

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/sharepoint_too/config.cfg'))

user = f"{config['default']['domain']}\\{config['default']['user']}"
pwd = config['default']['pwd']

site_url = config['default']['site_url']
weblist_url = config['default']['weblist_url']
list_title =  config['default']['list_title']
list_guid = config['default']['list_guid']
list_item_type = config['default']['list_item_type']

item_id = None

sp = SharePointSession(site_url, username=user, password=pwd)


# ------------------------------------------------------------------------------
# By GUID
# ------------------------------------------------------------------------------


def test_get_lists():
    r = sp.get_lists(weblist_url)
    assert r.status_code == 200


def test_get_list_metadata_by_guid():
    r = sp.get_list_metadata(weblist_url, list_guid=list_guid)
    assert r.status_code == 200


def test_get_list_items_by_guid():
    r = sp.get_list_items(weblist_url, list_guid=list_guid)
    assert r.status_code == 200


def test_add_list_item_by_guid():
    add_payload = {
        "__metadata": {"type": list_item_type},
        "Title": "ADDED remotely via rest api in python",
    }
    r = sp.add_list_item(weblist_url, payload=add_payload, list_guid=list_guid)
    assert r.status_code == 201
    print(r.json())

    # Set for use in future tests
    global item_id
    response = r.json()
    item_id = response["d"]["Id"]


def test_get_list_entity_type_by_guid():
    r = sp.get_list_entity_type(weblist_url, list_guid=list_guid)
    assert r.status_code == 200

    # global list_item_type
    response = r.json()
    list_item_type = response["d"]["ListItemEntityTypeFullName"]


def test_get_list_item_by_guid():
    r = sp.get_list_item(weblist_url, list_guid=list_guid, item_id=item_id)
    assert r.status_code == 200


def test_update_list_item_by_guid():
    update_payload = {
        "__metadata": {"type": list_item_type},
        "Title": "UPDATED remotely via rest api in python",
    }
    r = sp.update_list_item(weblist_url, item_id, update_payload, list_guid=list_guid)
    assert r.status_code == 204


def test_upload_by_guid():
    r = sp.upload(weblist_url, item_id, "tests/nda.pdf", list_guid=list_guid)
    print(r.json())
    assert r.status_code == 200


def test_delete_list_item_by_guid():
    r = sp.delete_list_item(weblist_url, item_id, list_guid=list_guid)
    assert r.status_code == 200


# ------------------------------------------------------------------------------
# By Title
# ------------------------------------------------------------------------------


def test_get_list_metadata_by_title():
    r = sp.get_list_metadata(weblist_url, list_title=list_title)
    assert r.status_code == 200


def test_get_list_items_by_title():
    r = sp.get_list_items(weblist_url, list_title=list_title)
    assert r.status_code == 200


def test_add_list_item_by_title():
    add_payload = {
        "__metadata": {"type": list_item_type},
        "Title": "ADDED remotely via rest api in python",
    }
    r = sp.add_list_item(weblist_url, payload=add_payload, list_title=list_title)
    print(r.json())
    assert r.status_code == 201

    # Set for use in future tests
    global item_id
    response = r.json()
    item_id = response["d"]["Id"]


def test_get_list_entity_type_by_title():
    r = sp.get_list_entity_type(weblist_url, list_title=list_title)
    assert r.status_code == 200

    # global list_item_type
    response = r.json()
    list_item_type = response["d"]["ListItemEntityTypeFullName"]


def test_get_list_item_by_title():
    r = sp.get_list_item(weblist_url, list_title=list_title, item_id=item_id)
    assert r.status_code == 200


def test_update_list_item_by_title():
    update_payload = {
        "__metadata": {"type": list_item_type},
        "Title": "UPDATED remotely via rest api in python",
    }
    r = sp.update_list_item(weblist_url, item_id, update_payload, list_title=list_title)
    assert r.status_code == 204


def test_upload_by_title():
    r = sp.upload(weblist_url, item_id, "tests/nda.pdf", list_title=list_title)
    print(r.json())
    assert r.status_code == 200


def test_delete_list_item_by_title():
    r = sp.delete_list_item(weblist_url, item_id, list_title=list_title)
    assert r.status_code == 200
