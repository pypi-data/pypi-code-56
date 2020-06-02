from .sessions import session_scope


def bulk_insert(engine, model, entries):
    """
    Bulk insert entries data to the database model/table.
    """
    with session_scope(engine) as session:
        session.bulk_insert_mappings(model, entries)
        session.commit()
