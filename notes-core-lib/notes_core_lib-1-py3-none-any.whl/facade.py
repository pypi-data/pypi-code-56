from . import services as s, notes_core as c, status as sta

def get_note(id):
    n = s.get_note(id)
    note = c.Note(label=n[1], priority=n[3], status=n[4], id=n[0], description=n[2], theme=n[5], start_date=n[7], finish_date=n[8])
    return note

def change_note_status(id, status):
    n = get_note(id)
    n.status = status
    s.update_note(n)

def change_note_theme(id, theme_id):
    n = get_note(id)
    n.theme = theme_id
    n.status = sta.Status(n.status)
    s.update_note(n)

