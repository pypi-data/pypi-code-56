# ==================================================================
#       文 件 名: doc.py
#       概    要: 生成数据库文档
#       作    者: IT小强 
#       创建时间: 6/9/20 5:52 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from ..base import doc


class Doc(doc.Doc):
    """
    生成数据库文档
    """

    def get_db_fields_info(self, table_name, cur_fields):
        """
        获取数据库中的字段信息
        :param table_name:
        :param cur_fields:
        :return:
        """

        sql = 'SHOW FULL COLUMNS FROM `' + table_name + '`'
        self.cursor.execute(sql)
        for filed_info in self.cursor.fetchall():
            cur_filed_info = {
                'field': filed_info[0],
                'type': filed_info[1],
                'collation': filed_info[2],
                'null': filed_info[3],
                'key': filed_info[4],
                'default': filed_info[5],
                'extra': filed_info[6],
                'privileges': filed_info[7],
                'comment': filed_info[8]
            }
            cur_fields[cur_filed_info['field']].update(cur_filed_info)
        return cur_fields
