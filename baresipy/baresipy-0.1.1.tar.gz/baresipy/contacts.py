from json_database import JsonDatabase
from os.path import expanduser, join, isdir
from os import makedirs


class ContactExists(ValueError):
    """ Choose new contact name """


class ContactDoesNotExist(ValueError):
    """ Choose new contact name """


class ContactList:
    def __init__(self, database_name="contacts.db"):
        db_dir = join(expanduser("~"), ".baresip")
        if not isdir(db_dir):
            makedirs(db_dir)
        self.db_path = join(db_dir, database_name)

    def search_contact(self, url):
        with JsonDatabase("contacts", self.db_path) as db:
            users = db.search_by_value("url", url)
            if len(users):
                return users[0]
        return None

    def is_contact(self, url):
        return self.search_contact(url) is not None

    def get_contact(self, name):
        with JsonDatabase("contacts", self.db_path) as db:
            users = db.search_by_value("name", name)
            if len(users):
                return users[0]
        return None

    def add_contact(self, name, url):
        if self.get_contact(name) is not None:
            raise ContactExists
        with JsonDatabase("contacts", self.db_path) as db:
            user = {"name": name, "url": url}
            db.add_item(user)

    def update_contact(self, name, url):
        contact = self.get_contact(name)
        if contact is None:
            raise ContactDoesNotExist

        with JsonDatabase("contacts", self.db_path) as db:
            item_id = db.get_item_id(contact)
            db.update_item(item_id, {"name": name, "url": url})

    def remove_contact(self, name):
        contact = self.get_contact(name)
        if contact is None:
            raise ContactDoesNotExist
        with JsonDatabase("contacts", self.db_path) as db:
            item_id = db.get_item_id(contact)
            db.remove_item(item_id)

    def print_contacts(self):
        with JsonDatabase("contacts", self.db_path) as db:
            db.print()
