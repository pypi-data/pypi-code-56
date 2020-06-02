import sys

import logging
logger = logging.getLogger(__name__)


class Core:

    _version = None
    _init_error = None

    def init(self, version=None):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        self._version = version
        if not Database.init():
            self._init_error = f'Error in {func_name}: not models.init())...'
            logger.error(self._init_error)
            return False
        return True

    @property
    def init_error(self):
        return self._init_error

    def get_footer(self):
        ver = 'not definded' if self._version is None else self._version
        return f'Vesion: {ver}'

    def get_cronjob_tasks(self):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        error = Database.test_session()
        if isinstance(error, str):
            return error
        try:
            cronjob_tasks = Database.session.query(Database.CronjobTask).all()
            if not isinstance(cronjob_tasks, list):
                error = f'Error in {func_name}: not isinstance(cronjob_tasks, list)...'
                logger.error(error)
                return error
            html_table = Database.get_html_table(cronjob_tasks, table=Database.CronjobTask)
            return html_table
        except Exception as e:
            error = f'Exception in {func_name}: {type(e)}: {str(e)}...'
            logger.exception(error)
            return error

    def update_cronjob_task(self, **kwargs):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        error = Database.test_session()
        if isinstance(error, str):
            return error
        if 'task_id' in kwargs:
            task_id = kwargs.get('task_id')
            del kwargs['task_id']
            cronjob_task = Database.session.query(Database.CronjobTask).filter_by(task_id=task_id).first()
            # print(f'{ models.get_dict_from_query(cronjob_task)}')
            if cronjob_task is None:
                error = f'Error in {func_name}: cronjob_task is None...'
                logger.error(error)
                return error
            Database.update_elem(cronjob_task, **kwargs)
            Database.session.commit()
            return Database.get_record_dict(cronjob_task)
        else:
            new_cronjob_task = Database.CronjobTask(**kwargs)
            Database.session.add(new_cronjob_task)
            Database.session.commit()
            return Database.get_record_dict(new_cronjob_task)

    def get_tasks(self):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        error = Database.test_session()
        if isinstance(error, str):
            return error
        try:

            task_columns = list(Database.get_table_columns(Database.Task()).keys())

            def remove_from_list(_list, _remove_list):
                for _val in _remove_list:
                    if _val in _list:
                        _list.remove(_val)
            remove_from_list(task_columns, ['defer_time', 'failed_email', 'success_email', 'parent_task_id'])
            # from sqlalchemy.orm import load_only
            # tasks = models.session.query(models.Task).options(load_only('defer_time', 'failed_email')).all()
            tasks = Database.session.query(Database.Task).all()
            if not isinstance(tasks, list):
                error = f'Error in {func_name}: not isinstance(tasks, list)...'
                logger.error(error)
                return error
            html_table = Database.get_html_table(tasks, columns=task_columns, table=Database.Task)
            return html_table
        except Exception as e:
            error = f'Exception in {func_name}: {type(e)}: {str(e)}...'
            logger.exception(error)
            return error

    def update_task(self, **kwargs):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        error = Database.test_session()
        if isinstance(error, str):
            return error
        if 'task_id' in kwargs:
            task_id = kwargs.get('task_id')
            del kwargs['task_id']
            task = Database.session.query(Database.Task).filter_by(task_id=task_id).first()
            # print(f'{ models.get_dict_from_query_one(task)}')
            if task is None:
                error = f'Error in {func_name}: task is None...'
                logger.error(error)
                return error
            Database.update_elem(task, **kwargs)
            Database.session.commit()
            return Database.get_record_dict(task)
        else:
            error = f'Error in {func_name}: "task_id" not in kwargs'
            logger.error(error)
            return error


core = Core()
