import sys
from croniter import croniter
import datetime
import time
from sqlalchemy import and_
from pg_tasks_queue.Config import cfg as config
from pg_tasks_queue.Logging import init_logger
import pg_tasks_queue.Database as database

import logging
logger = logging.getLogger(__name__)


class CronJobTasks:

    _started = False

    def update_tasks(self):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'

        now = datetime.datetime.now()
        logger.info(f'Start {func_name} at {now}')

        if not database.get_session():
            error = f'Error in {func_name}: not database.get_session()...'
            logger.error(error)
            return error

        if database.project:
            filter_value = and_(database.CronjobTask.project == database.project,
                                database.CronjobTask.enabled.is_(True))
        else:
            filter_value = database.CronjobTask.enabled.is_(True)

        cronjob_tasks = database.session.query(database.CronjobTask).filter(filter_value).all()
        database.session.commit()

        if not isinstance(cronjob_tasks, list):
            error = f'Error in {func_name}: not isinstance(cronjob_tasks, list)...'
            logger.error(error)
            return error

        start_of_min = datetime.datetime.strptime(now.strftime('%Y-%m-%d %H:%M:00'), '%Y-%m-%d %H:%M:00')

        for cronjob_task in cronjob_tasks:

            itr = croniter(cronjob_task.schedule, start_of_min)
            scheduled_time = itr.get_next(datetime.datetime)

            if database.project:
                filter_value = and_(database.Task.project == database.project,
                                    database.Task.cronjob_task_id == cronjob_task.task_id,
                                    database.Task.scheduled_time > start_of_min)

            else:
                filter_value = and_(database.Task.cronjob_task_id == cronjob_task.task_id,
                                    database.Task.scheduled_time > start_of_min)

            task = database.session.query(database.Task).filter(filter_value).first()
            database.session.commit()

            if task is None:
                logger.info(f'{func_name}; apply cronjob_task   : {cronjob_task}')
                cronjob_task.last_start_time = cronjob_task.next_start_time
                cronjob_task.next_start_time = scheduled_time
                database.session.commit()
                logger.info(f'{func_name}; updated cronjob_task : {cronjob_task}')
                new_task_dict = {'priority': 1,
                                 'create_time': start_of_min,
                                 'scheduled_time': scheduled_time,
                                 'cronjob_task_id': cronjob_task.task_id}
                task_columns = list(database.get_table_columns(database.Task()).keys())
                task_columns.remove('task_id')
                for task_column in task_columns:
                    if task_column in cronjob_task.__table__.columns:
                        new_task_dict[task_column] = getattr(cronjob_task, task_column)
                new_task = database.add_task(new_task_dict)
                logger.info(f'{func_name}; create new task      : {new_task}')

        database.close_session()

        return None

    def start(self, cfg=None):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'

        raise_exception = False
        try:

            if cfg is None:
                if not isinstance(config.cfg, dict):
                    logger.error(f'Error in {func_name}: not isinstance(config.cfg, dict)...')
                    return
                cfg = config.cfg

            if not database.init(cfg.get('database')):
                logger.error(f'Error in {func_name}: not database.init()...')
                return

            sleep_sec = None
            loops_limit = 1
            life_timeout_sec = None

            cronjobs_cfg = cfg.get('cronjobs')
            if isinstance(cronjobs_cfg, dict):
                raise_exception = cronjobs_cfg.get('raise_exception', raise_exception)

                if cronjobs_cfg.get('sleep_sec') is not None:
                    sleep_sec = float(cronjobs_cfg.get('sleep_sec'))

                if cronjobs_cfg.get('life_timeout_sec') is not None:
                    life_timeout_sec = float(cronjobs_cfg.get('life_timeout_sec'))

                if cronjobs_cfg.get('loops_limit') is not None:
                    loops_limit = int(cronjobs_cfg.get('loops_limit'))

            started_timestamp = datetime.datetime.now()
            loops_counter = 0
            self._started = True
            while self._started:
                self.update_tasks()
                loops_counter += 1
                if loops_limit and loops_counter >= loops_limit:
                    logger.info(f'{func_name}; loops_counter({loops_counter})'
                                f' == loops_limit({loops_limit}) => break...')
                    break
                elif life_timeout_sec is not None:
                    time_delta = datetime.datetime.now() - started_timestamp
                    time_delta_sec = time_delta.total_seconds()
                    if time_delta_sec > life_timeout_sec:
                        logger.info(f'{func_name}; time_delta_sec({time_delta_sec})'
                                    f' > life_timeout_sec({life_timeout_sec}) => break...')
                        break
                time.sleep(sleep_sec)

        except Exception as e:
            logger.exception(f'Error in {func_name}: {type(e)}: {str(e)}...')
            if raise_exception:
                raise e

    def stop(self):
        self._started = False


if __name__ == '__main__':
    name = 'CronJob Tasks'
    ver = '1.2'
    release_date = '2020-06-05 10:25'
    version = f'{name}. ver: {ver} ({release_date})'
    init_logger()

    logger.warning(f'Start {version}')
    CronJobTasks().start(config.cfg)
    logger.warning(f'End {version}')
