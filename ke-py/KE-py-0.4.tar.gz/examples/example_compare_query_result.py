# coding=u8
import os
from KE import KE
import itertools
import csv
from collections import OrderedDict

"""
VIVO KE3 迁移到 KE4，上线前需要拿一部分历史查询，对比查询结果准确性。

输出一个general_result.csv：
1）一致性比对结果CSV文件（项目，SQL，查询状态（3X，4X），查询对象（3X，4X），查询ID（3X，4X），响应时间（3X，4X），结果条数（3X，4X），结果是否一致，结果不一致开始坐标（行列）按列遍历 

对查询不一致的SQL 输出3x 4x 各一个结果明细的CSV：
结果不一致的查询每条查询生成2个CSV文件（查询ID_3X.csv,查询ID_4X.csv)，文件中为整个查询结果。

"""

client3 = KE('device2', username='admin', password='Kyligence@2020', version=3)
client4 = KE('10.1.3.63', port=7171, username='ADMIN', password='KYLIN', version=4)

sql = "select PART_DT, count(1) from kylin_sales group by PART_DT;"
project = 'learn_kylin'

res3 = client3.query(sql, project=project)
res4 = client4.query(sql, project=project)


def compare_list(list1, list2):
    counter = 0
    for e1, e2 in itertools.zip_longest(list1, list2):
        if e1 != e2:
            print(e1, e2)
            return counter
        counter += 1


def compare_df(df1, df2):
    is_same = True
    coordinate = tuple()

    for col1, col2 in zip(df1, df2):
        data1 = sorted(list(df1[col1]))
        data2 = sorted(list(df2[col1]))
        print(col1, col2)
        is_col_same = (data1 == data2)
        if not is_col_same:
            is_same = False
            index = compare_list(data1, data2)
            coordinate = (col1, index)
            return is_same, coordinate
    return is_same, coordinate


def get_general(query_id, sql, project):
    result = OrderedDict()
    res3 = client3.query(sql, project=project)
    res4 = client4.query(sql, project=project)

    result['qid'] = query_id
    result['sql'] = sql
    result['project'] = project
    result['realization3'] = res3.cube

    result['duration3'] = res3.duration
    result['duration4'] = res4.duration

    result['isException3'] = res3.isException
    result['isException4'] = res4.isException

    result['pushDown3'] = res3.pushDown
    result['pushDown4'] = res4.pushDown

    result['timeout3'] = res3.timeout
    result['timeout4'] = res4.timeout

    result['rows3'] = res3.df.shape[0]
    result['rows4'] = res4.df.shape[0]

    is_same, coordinate = compare_df(res3.df, res4.df)
    result['is_same'] = is_same
    result['coordinate'] = coordinate

    return result


general_csv_path = '/Users/xifeng.li/test/general_result.csv'

if os.path.exists(general_csv_path):
    pass
else:
    with open(general_csv_path, 'w') as file:
        pass

general_history = open(general_csv_path, 'r').read()


def check_qid_exist(qid):
    """检查query_id是否已经在CSV文件里"""
    if qid in general_history:
        return True
    return False


def write2csv(result):
    with open(general_csv_path, 'w', encoding='utf-8') as f:
        for query_id, sql, project in ["iterator"]:
            exist = check_qid_exist(query_id)
            if exist:
                continue
            result = get_general(query_id, sql, project)
            writer = csv.DictWriter(f, result.keys(), delimiter='|')
            writer.writerow(result)
