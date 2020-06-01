from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from bookmark.sql_bookmarker import SQLAlchemyBookmarker

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URI", "sqlite://")
db = SQLAlchemy(app)
sql_bookmarker = SQLAlchemyBookmarker(db)
db.create_all()


def test_bookmark():
    sql_bookmarker["abc"] = "123"
    assert sql_bookmarker.get("abc") == "123"


def test_bookmark_with_none_value():
    assert not sql_bookmarker.get("xyz")
    sql_bookmarker["xyz"] = None
    assert not sql_bookmarker.get("xyz")
