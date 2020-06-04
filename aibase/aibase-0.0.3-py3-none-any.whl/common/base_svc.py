# -*- coding: utf-8 -*-
# @Time: 2020/05/13
# @Author: gmo_ye
# @Version: 1.0.0
# @Function:
import json

from aibase.common import logger
from aibase.common.comm_define import ResponseCode, ActiveException


def result_wrap(code=ResponseCode.OK, message=ResponseCode.OK_MSG, data=None):
    """
        返回值封装
    :param code: 返回码
    :param message: 消息
    :param data: 数据
    :return: json格式返回值
    """
    if data:
        result = json.dumps({'errorCode': code, 'errorMsg': message, 'data': data}, ensure_ascii=False)
    else:
        result = json.dumps({'errorCode': code, 'errorMsg': message}, ensure_ascii=False)
    return result


def check_param_required(param_key, param_value):
    """
        校验参数必填
    :param param_key: 参数名
    :param param_value: 参数值
    :return: 封装返回结果
    """
    if param_value is None:
        error_message = ResponseCode.MSG_MISS_PARAM + param_key
        logger.error(error_message)
        raise ActiveException(code=ResponseCode.PARAM_ERROR, msg=error_message)


def check_page_params(param):
    """
        分页查询参数校验
    :param param: 参数
    :return: (校验是否通过, 校验信息, page_no, page_size)
    """
    page_no = 0
    page_size = 20
    if param is not None:
        try:
            page_params = json.loads(param)
            page_no = page_params.get('pageNo', 0)
            page_size = page_params.get('pageSize', 20)
        except Exception:
            raise ActiveException(code=ResponseCode.ILLEGAL_OPERATION, msg=ResponseCode.MSG_PAGE_ERROR)
    if not isinstance(page_no, int) or not isinstance(page_size, int):
        raise ActiveException(code=ResponseCode.ILLEGAL_OPERATION, msg=ResponseCode.MSG_PAGE_ERROR)
    return True, None, page_no, page_size


__all__ = ['result_wrap', 'check_param_required', 'check_page_params']
