from abc import ABC

from django.db.backends.mysql.schema import DatabaseSchemaEditor as MySqlDatabaseSchemaEditor


class DatabaseSchemaEditor(MySqlDatabaseSchemaEditor, ABC):

    def column_sql(self, model, field, include_default=False):
        """
        重写 字段sql生成方法
        :param model:
        :param field:
        :param include_default:
        :return:
        """

        # 字段默认值是否写入到sql语句中处理，可在settings.py中配置
        include_default_fun = self.connection.settings_dict.get('INCLUDE_DEFAULT', None)
        if include_default is not None:
            include_default = include_default_fun(model, field, include_default, self.connection)

        # 生成sql
        sql, params = super().column_sql(model, field, include_default)

        # 写入字段注释
        if field.help_text:
            sql += " COMMENT '%s'" % field.help_text
        elif field.verbose_name:
            sql += " COMMENT '%s'" % field.verbose_name
        return sql, params

    def table_sql(self, model):
        """
        重写表sql生成方法
        :param model:
        :return:
        """
        sql, params = super().table_sql(model)
        if model._meta.verbose_name:
            sql += " COMMENT '%s'" % model._meta.verbose_name
        return sql, params
