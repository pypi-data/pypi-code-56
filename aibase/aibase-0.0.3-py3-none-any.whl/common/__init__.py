# -*- coding: utf-8 -*-
# @Time: 2020/6/3 0003
# @Author: gmo_ye
# @Version: 1.0.0
# @Function:
from aibase.common import project_path as _project_path

project_root_path = _project_path.__init_project_path()
project_src_path = _project_path.__project_path
relative_project_path = _project_path.relative_project_path
cfg_path = _project_path.cfg_path

from aibase.common import logger as _logger

logger = _logger.Logger().logger

from aibase.common import base_svc as _base_svc

result_wrap = _base_svc.result_wrap
check_page_params = _base_svc.check_page_params
check_param_required = _base_svc.check_param_required
