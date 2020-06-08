
from textwarden import TwException
from textwarden import database as db
import json
import logging
import textwrap
import time

logger = logging.getLogger(__name__)

def MultipleUsersMatched(TwException):
    """
    Request did not result in a unique user. Multiple users found.
    """
    pass

def find_by_uuid(uuid):
    res = db.execute('''
        SELECT * FROM users WHERE uuid=?;
        ''',(
        str(uuid),
        ))
    if len(res) == 0:
        return None
    return User(res[0][0], res[0][1])

class User(object):
    def __init__(self, uuid):
        self.uuid = str(uuid)
        self.data = {}
        self.load()

    def __str__(self):
        return "uuid:{}\n{}".format(
                self.uuid,
                json.dumps(self.data),
                )

    def load(self):
        res = db.execute('''
            SELECT * FROM users WHERE uuid=?;
            ''',(
            self.uuid,
            ))
        if len(res) > 0:
            self.data = json.loads(res[0][1])
            return True
        return False
    
    def save(self):
        res = db.execute('''
            INSERT INTO users(uuid, data)
            VALUES(?, ?);
            ''',(
            self.uuid,
            json.dumps(self.data),
            ))
        return True
  
    def update(self):
        res = db.execute('''
            UPDATE users
            SET data=?
            WHERE uuid=?
            ''',(
            json.dumps(self.data),
            self.uuid,
            ))
 
    def access(self):
        time_now = time.time()
        self.data["time_accessed"] = time_now
        self.update()

