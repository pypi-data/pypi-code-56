# -*- coding: utf-8 -*-
# @Time: 2020/05/13
# @Author: gmo_ye
# @Version: 1.0.0
# @Function: 公共定义


class ResponseCode:
    # 正常结果码
    OK = 0
    # 正常返回内容
    OK_MSG = 'success'

    # 异常错误
    ABNORMAL = 10200
    # 参数错误
    PARAM_ERROR = 10201
    # 非法操作
    ILLEGAL_OPERATION = 10202

    # 参数缺失
    MSG_MISS_PARAM = 'missing parameter:'
    # 分页参数错误
    MSG_PAGE_ERROR = 'Page parameter error'
    # json 格式错误
    MSG_JSON_ERROR = 'Json format error'


class ActiveException(Exception):
    def __init__(self, code=ResponseCode.ABNORMAL, msg=str(Exception)):
        self.code = code
        self.msg = msg

    def get_info(self):
        return self.code, self.msg

