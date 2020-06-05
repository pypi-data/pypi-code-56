from re import sub
from pwx_db import PostgresDB, Native


class PersistSync:

    __slots__ = ['__table_name', '__columns', '__values', '__sql_delete', '__sql_insert', '__ids']

    __db = PostgresDB()

    def __init__(self, table_name):
        self.__table_name = table_name
        self.__ids = []

    def __init(self, columns, values, only_insert):
        self.__columns = columns
        self.__values = values

        if not only_insert:
            self.__get_ids()

    def persist(self, columns, values, many=False, only_insert=False):
        self.__init(columns, values, only_insert)
        self.__prepare_sql(many, only_insert)
        self.__execute(only_insert)
        self.__ids = []

    def __get_ids(self):
        if isinstance(self.__values[0], list):
            for value in self.__values:
                self.__ids.append(int(value[0]))  # first position always be id
        else:
            self.__ids.append(self.__values[0])

    def __prepare_sql(self, many, only_insert):
        if not only_insert:
            self.__sql_delete = Native.delete_by_id(table_name=self.__table_name, ident=self.__get_string(self.__ids))

        self.__sql_insert = Native.insert(table_name=self.__table_name,
                                          colunms=self.__get_string(self.__columns, is_columns=True),
                                          values=self.__get_string(self.__values, many))

    def __get_string(self, values, many=False, is_columns=False):
        if many:
            return self.__many_values(values, is_columns)

        return self.__to_string(values, is_columns)

    def __to_string(self, values, is_columns):
        return f"({', '.join([self.__convert(value, is_columns) for value in values])})"

    @staticmethod
    def __convert(value, is_columns):
        if is_columns:
            return str(value)

        elif isinstance(value, bool):
            return "'" + f'{str(value).lower()}' + "'"

        elif isinstance(value, int) or isinstance(value, float):
            return str(value)

        elif isinstance(value, str):
            return "'" + f'{value.lower()}' + "'"

        elif not value:
            return 'null'

    def __many_values(self, values, is_columns):
        val = ''
        for value in values:
            val += f'{self.__to_string(value, is_columns)},'

        return sub('[,]$', ';', val)

    def __execute(self, only_insert):
        if not only_insert:
            self.__execute_delete()

        self.__execute_insert()

    def __execute_delete(self):
        self.__db.execute_query(sql=self.__sql_delete)

    def __execute_insert(self):
        self.__db.execute_query(sql=self.__sql_insert)
