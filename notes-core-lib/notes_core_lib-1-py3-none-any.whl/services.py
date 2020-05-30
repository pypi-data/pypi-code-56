from . import config
from . import dbservice
from . import status as s
from . import predicate as p

SELECT_NOTE = "SELECT * FROM note WHERE id = %s"
INSERT_NOTE = "INSERT INTO note(label, description, priority, status, theme, creation_datetime, start_date, finish_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
UPDATE_NOTE = "UPDATE note SET label = %s, description = %s, status = %s, theme = %s WHERE id = %s"
DELETE_NOTE = "DELETE FROM note WHERE id = %s"
FILTER_NOTE = "SELECT * FROM note WHERE "
SELECT_STATUS_BY_ID = "SELECT * FROM status WHERE id = %s"
SELECT_ALL_STATUSES = "SELECT * FROM status"
SELECT_THEME_BY_ID = "SELECT * FROM theme WHERE id = %s"
SELECT_ALL_THEMES = "SELECT * FROM theme"
INSERT_THEME = "INSERT INTO theme (label) VALUES (%s) RETURNING id"
UPDATE_THEME = "UPDATE theme SET label = %s WHERE id = %s"
DELETE_THEME = "DELETE FROM theme WHERE id = %s"
SELECT_ALL_NOTES = "SELECT * FROM note"
SELECT_ALL_NOTES_LIST = "SELECT * FROM all_notes"

# Services for notes

def get_note(id):
    if id is None:
        raise ValueError

    note = dbservice.select_one(SELECT_NOTE, (id,))
    return note

def get_notes():
    notes = dbservice.select_all(SELECT_ALL_NOTES)
    return notes

def get_all_notes_list():
    all_notes = dbservice.select_all(SELECT_ALL_NOTES_LIST)
    return all_notes

def store_note(note):
    if note is None:
        raise ValueError

    id = dbservice.execute_with_return(INSERT_NOTE, (note.label, note.description, note.priority.value[0], note.status.value, note.theme, note.creation_datetime, note.start_date, note.finish_date))
    dbservice.commit()
    return id

def update_note(note):
    if note is None:
        raise ValueError

    dbservice.execute(UPDATE_NOTE, (note.label, note.description, note.status.value, note.theme, note.id))
    dbservice.commit()

def remove_note(id):
    if id is None:
        raise ValueError

    dbservice.execute(DELETE_NOTE, (id,))
    dbservice.commit()

def filter_notes(predicate):
    if predicate is None:
        raise ValueError
    
    query = FILTER_NOTE + predicate.toQuery()
    notes = dbservice.select_all(query)
    return notes

# Services for statuses

def get_status(id):
    if id is None:
        raise ValueError
    
    status = s.Status(id)
    return status

def _load_statuses():
    statuses = dbservice.select_all(SELECT_ALL_STATUSES)
    return statuses

def get_full_status(id):
    full_statuses = _load_statuses()
    full_status = next(stat for stat in full_statuses if stat[0] == id)
    return full_status

def get_full_statuses():
    return full_statuses

def get_status_label(status):
    return get_full_status(status.value)[2]

# Services for themes

def get_theme(id):
    if id is None:
        raise ValueError
    
    theme = dbservice.select_one(SELECT_THEME_BY_ID, (id,))
    return theme

def get_themes():
    themes = dbservice.select_all(SELECT_ALL_THEMES)
    return themes

def store_theme(label):
    if label is None:
        raise ValueError

    id = dbservice.execute_with_return(INSERT_THEME, (label,))
    dbservice.commit()
    return id

def update_theme(id, label):
    if id is None or label is None:
        raise ValueError

    dbservice.execute(UPDATE_THEME, (label, id))
    dbservice.commit()

def remove_theme(id):
    if id is None:
        raise ValueError

    dbservice.execute(DELETE_THEME, (id,))
    dbservice.commit()

