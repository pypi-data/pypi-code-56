class Native:
    __slots__ = []

    @staticmethod
    def delete_by_id(table_name, ident):
        return f'DELETE FROM {table_name} where id IN {ident}'

    @staticmethod
    def insert(table_name, colunms, values):
        return f'INSERT INTO {table_name}{colunms} VALUES{values}'
