from datetime import datetime
from typing import Optional

import pytz
from sqlalchemy import func

from bookmark import Bookmarker


def get_bookmark_model(db):
    class BookmarkModel(db.Model):
        __tablename__ = "_bookmark"

        bookmark_value = db.Column(db.String, nullable=True)
        bookmark_key = db.Column(db.String, primary_key=True, nullable=False)
        updated_at = db.Column(
            db.DateTime, nullable=False, default=func.now(), onupdate=func.now()
        )
        created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    return BookmarkModel


class SQLAlchemyBookmarker(Bookmarker):
    def __init__(self, db):
        self._model = get_bookmark_model(db)
        self._db = db

    def get(self, key: str) -> Optional[str]:
        bookmark = (
            self._db.session.query(self._model)
            .filter(self._model.bookmark_key == key)
            .one_or_none()
        )
        if not bookmark:
            return None

        return bookmark.bookmark_value

    def __setitem__(self, key: str, value: str):
        self._update(key=key, value=value)

    def _update(self, key: str, value: str):
        time_now = pytz.utc.localize(datetime.utcnow())
        cs_cursor = self._model(
            bookmark_key=key, bookmark_value=value, updated_at=time_now
        )
        self._db.session.merge(cs_cursor)
        self._db.session.commit()
