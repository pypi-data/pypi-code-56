import os
import sys
import json
import importlib.util
import time
import threading
import queue
import datetime
import multiprocessing
import traceback
from pg_tasks_queue.Config import cfg as config
import pg_tasks_queue.Database as database
from pg_tasks_queue.Kthread import KThread as kthread

import logging
logger = logging.getLogger(__name__)


class Worker:

    _blocking = True
    _sleep_sec = None
    _timeout_sec = 600.
    _life_timeout_sec = None
    _started = False
    _started_timestamp = None
    _worker = None
    _current_task = None
    _raise_exception = False

    def check_module(self, module_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        module_spec = importlib.util.find_spec(module_name)
        if module_spec is None:
            logger.error(f'Error in {func_name}: module: "{module_name}" not found')
            return None
        else:
            return module_spec

    def import_module(self, module_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        module_spec = self.check_module(module_name)
        if module_spec is None:
            return None
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    def import_function_from_module(self, module_name, function_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        module = self.import_module(module_name)
        if module is None:
            return None
        if not hasattr(module, function_name):
            logger.error(f'Error in {func_name}: module: "{module_name}"; function: "{function_name}" not found')
            return None
        return getattr(module, function_name)

    def worker(self, task_dict):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        # print(f'{func_name}; os.getpid(): {os.getpid()}; os.getppid(): {os.getppid()}')
        task_module = task_dict.get('module')
        task_func = task_dict.get('func')
        func = self.import_function_from_module(task_module, task_func)
        if func is None:
            error = f'Error in {func_name}: import_function_from_module({task_module}, {task_func}) is None'
            logger.error(error)
            return {'status': 'error', 'result': error}
        else:
            params = task_dict.get('params')
            if isinstance(params, str):
                params = json.loads(params)
            if not isinstance(params, dict):
                params = dict()
            logger.info(f'Started task (id={task_dict.get("task_id")}) at {datetime.datetime.now()}; task_dict: {task_dict}')
            res = func(**params)
            logger.info(f'Finished task (id={task_dict.get("task_id")}) at {datetime.datetime.now()}; result: {res}')
            return res

    def worker_process(self, queue, task_dict):
        result = self.worker(task_dict)
        queue.put(result)

    def stop_woker(self, func_name):
        error = f'Error in {func_name}: worker.is_alive() => os.kill(os.getpid(), signal.SIGINT)'
        if self._worker:
            database.set_worker_error(error, self._worker, self._current_task)
        try:
            # sys.exit(1)
            import signal
            os.kill(os.getpid(), signal.SIGINT)
        finally:
            logger.error(error)

    def _do_task(self, process_type):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        # print(f'{func_name}; os.getpid(): {os.getpid()}; os.getppid(): {os.getppid()}')
        if not self._started:
            logger.warning(f'{func_name}; self._started = False; return')
            return

        exception = None
        error = None
        timer = None
        try:
            self._current_task = database.get_new_task(self._worker)
            if isinstance(self._current_task, str):
                logger.error(f'Error in {func_name}; {self._current_task}')
                return
            elif self._current_task is None:
                return

            # print(f'{func_name}: now={datetime.datetime.now()}; task: {self._current_task}')
            task_dict = database.get_record_dict(self._current_task)
            if process_type is None:
                # timer = threading.Timer(self._timeout_sec, self.stop_woker, args=(func_name,))
                # timer.setDaemon(False)
                # timer.start()
                result_dict = self.worker(task_dict)
                # timer.cancel()
                database.update_worker_task(result_dict, self._current_task, self._worker)
            elif process_type in ['fork', 'thread', 'kthread']:
                if process_type == 'fork':
                    worker_queue = multiprocessing.Queue()
                    worker = multiprocessing.Process(target=self.worker_process, args=(worker_queue, task_dict,))
                else:
                    worker_queue = queue.Queue()
                    if process_type == 'thread':
                        worker = threading.Thread(target=self.worker_process, args=(worker_queue, task_dict,))
                        worker.setDaemon(True)
                    else:
                        worker = kthread(target=self.worker_process, args=(worker_queue, task_dict,))
                worker.start()
                worker.join(timeout=self._timeout_sec)
                if worker.is_alive():
                    if process_type in ['fork', 'kthread']:
                        worker.terminate()
                        error = f'Error in {func_name}: worker({process_type}).is_alive() => worker.terminate()'
                        logger.error(error)
                        database.update_worker_task({'status': 'error', 'result': error}, self._current_task,
                                                    self._worker)
                    else:
                        error = f'Error in {func_name}: worker({process_type}).is_alive() => sys.exit(1)'
                        logger.error(error)
                        if self._worker:
                            database.set_worker_error(error, self._worker, self._current_task)
                        sys.exit(1)
                else:
                    if not worker_queue.empty():
                        database.update_worker_task(worker_queue.get_nowait(), self._current_task, self._worker)
                    else:
                        error = f'Error in {func_name}: queue is empty()...'
                        logger.error(error)
                        database.update_worker_task({'status': 'error', 'result': error}, self._current_task,
                                                    self._worker)

        except Exception as e:
            exception = e
            error = f'Exception in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.format_exc()}'
        finally:
            if timer:
                timer.cancel()
            if exception:
                if self._raise_exception:
                    if self._worker:
                        database.set_worker_error(error, self._worker, self._current_task)
                    raise exception
                else:
                    database.update_worker_task({'status': 'error', 'result': error}, self._current_task,
                                                self._worker)
                    logger.error(error)
            if not self._blocking:
                if self._life_timeout_sec is not None:
                    time_delta = datetime.datetime.now() - self._started_timestamp
                    time_delta_sec = time_delta.total_seconds()
                    if time_delta_sec > self._life_timeout_sec:
                        logger.info(f'{func_name}; time_delta_sec({time_delta_sec})'
                                    f' > life_timeout_sec({self._life_timeout_sec}) => return...')
                        if self._worker:
                            self._worker.status = 'finished'
                            self._worker.finished_time = datetime.datetime.now()
                            database.session.commit()
                        return
                threading.Timer(self._sleep_sec, self._do_task, args=(process_type,)).start()

    def _do_current_task(self, process_type):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        # print(f'{func_name}; os.getpid(): {os.getpid()}; os.getppid(): {os.getppid()}')
        if not self._started:
            logger.warning(f'{func_name}; self._started = False; return')
            return

        exception = None
        error = None
        timer = None
        try:
            # print(f'{func_name}: now={datetime.datetime.now()}; task: {self._current_task}')
            task_dict = database.get_record_dict(self._current_task)
            if process_type is None:
                # timer = threading.Timer(self._timeout_sec, self.stop_woker, args=(func_name,))
                # timer.setDaemon(False)
                # timer.start()
                result_dict = self.worker(task_dict)
                # timer.cancel()
                database.update_worker_task(result_dict, self._current_task, self._worker)
            elif process_type in ['fork', 'thread', 'kthread']:
                if process_type == 'fork':
                    worker_queue = multiprocessing.Queue()
                    worker = multiprocessing.Process(target=self.worker_process, args=(worker_queue, task_dict,))
                else:
                    worker_queue = queue.Queue()
                    if process_type == 'thread':
                        worker = threading.Thread(target=self.worker_process, args=(worker_queue, task_dict,))
                        worker.setDaemon(True)
                    else:
                        worker = kthread(target=self.worker_process, args=(worker_queue, task_dict,))
                worker.start()
                worker.join(timeout=self._timeout_sec)
                if worker.is_alive():
                    if process_type in ['fork', 'kthread']:
                        worker.terminate()
                        error = f'Error in {func_name}: worker({process_type}).is_alive() => worker.terminate()'
                        logger.error(error)
                        database.update_worker_task({'status': 'error', 'result': error}, self._current_task,
                                                    self._worker)
                    else:
                        error = f'Error in {func_name}: worker({process_type}).is_alive() => sys.exit(1)'
                        logger.error(error)
                        if self._worker:
                            database.set_worker_error(error, self._worker, self._current_task)
                        sys.exit(1)
                else:
                    if not worker_queue.empty():
                        database.update_worker_task(worker_queue.get_nowait(), self._current_task, self._worker)
                    else:
                        error = f'Error in {func_name}: queue is empty()...'
                        logger.error(error)
                        database.update_worker_task({'status': 'error', 'result': error}, self._current_task,
                                                    self._worker)

        except Exception as e:
            exception = e
            error = f'Exception in {func_name}: {type(e)}: {str(e)}; traceback: {traceback.format_exc()}'
        finally:
            if timer:
                timer.cancel()
            if exception:
                if self._raise_exception:
                    if self._worker:
                        database.set_worker_error(error, self._worker, self._current_task)
                    database.close_session()
                    raise exception
                else:
                    database.update_worker_task({'status': 'error', 'result': error}, self._current_task,
                                                self._worker)
                    logger.error(error)

    def _do_tasks(self, process_type, task_limit):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        if not self._started:
            logger.warning(f'{func_name}; self._started = False; return')
            return

        if not database.get_session():
            logger.error(f'Error in {func_name}: not database.get_session()...')
            return

        new_tasks = database.get_new_tasks(task_limit, self._worker)
        if isinstance(self._current_task, str):
            logger.error(f'Error in {func_name}; {new_tasks}')
            return

        for task in new_tasks:
            task.started_time = datetime.datetime.now()
            if self._worker:
                self._worker.current_task_id = task.task_id
            database.session.commit()
            self._current_task = task
            self._do_current_task(process_type)

        if self._worker:
            self._worker.current_task_id = None

        database.session.commit()
        database.close_session()

        if not self._blocking:
            if self._life_timeout_sec is not None:
                time_delta = datetime.datetime.now() - self._started_timestamp
                time_delta_sec = time_delta.total_seconds()
                if time_delta_sec > self._life_timeout_sec:
                    logger.info(f'{func_name}; time_delta_sec({time_delta_sec})'
                                f' > life_timeout_sec({self._life_timeout_sec}) => return...')
                    if self._worker:
                        self._worker.status = 'finished'
                        self._worker.finished_time = datetime.datetime.now()
                        database.session.commit()
                    return
            threading.Timer(self._sleep_sec, self._do_task, args=(process_type,)).start()

    def start(self, cfg=None, config_id=None):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'

        if cfg is None:
            if not isinstance(config.cfg, dict):
                logger.error(f'Error in {func_name}: not isinstance(config.cfg, dict)...')
                return
            cfg = config.cfg

        if not database.init(cfg.get('database')):
            logger.error(f'Error in {func_name}: not database.init()...')
            return

        if not database.get_session():
            error = f'Error in {func_name}: not database.get_session()...'
            logger.error(error)
            return error

        process_type = None
        task_limit = 20
        loops_limit = 1
        create_db_worker = False
        worker_cfg = cfg.get('worker')

        if not isinstance(worker_cfg, dict):
            worker_cfg = dict()

        if 'sleep_sec' in worker_cfg:
            worker_cfg['sleep_sec'] = float(worker_cfg.get('sleep_sec'))
        if 'timeout_sec' in worker_cfg:
            worker_cfg['timeout_sec'] = float(worker_cfg.get('timeout_sec'))
        if 'life_timeout_sec' in worker_cfg:
            worker_cfg['life_timeout_sec'] = float(worker_cfg.get('life_timeout_sec'))
        if 'loops_limit' in worker_cfg:
            worker_cfg['loops_limit'] = int(worker_cfg.get('loops_limit'))
        if 'task_limit' in worker_cfg:
            worker_cfg['task_limit'] = int(worker_cfg.get('task_limit'))

        if config_id is not None:
            db_cfg = database.session.query(database.Config).filter(
                database.Config.config_id == config_id).first()
            if db_cfg is None:
                db_cfg = database.Config(config_id=config_id, config=worker_cfg)
                database.add_new_record(db_cfg, database.Config)
            else:
                for key in worker_cfg.keys():
                    if key in db_cfg.config:
                        worker_cfg[key] = db_cfg.config.get(key)
                for key in db_cfg.config.keys():
                    if key not in worker_cfg:
                        worker_cfg[key] = db_cfg.config.get(key)

        if 'enabled' in worker_cfg:
            if worker_cfg.get('enabled', True) is False:
                logger.warning(f'Error in {func_name}: enabled if False => return...')
                database.close_session()
                return

        if 'blocking' in worker_cfg:
            self._blocking = worker_cfg.get('blocking', self._blocking)
        if 'raise_exception' in worker_cfg:
            self._raise_exception = worker_cfg.get('raise_exception', self._raise_exception)
        if 'sleep_sec' in worker_cfg:
            self._sleep_sec = worker_cfg.get('sleep_sec')
        if 'timeout_sec' in worker_cfg:
            self._timeout_sec = worker_cfg.get('timeout_sec')
        if 'life_timeout_sec' in worker_cfg:
            self._life_timeout_sec = worker_cfg.get('life_timeout_sec')
        if 'loops_limit' in worker_cfg:
            loops_limit = worker_cfg.get('loops_limit')
        if 'task_limit' in worker_cfg:
            task_limit = worker_cfg.get('task_limit')

        if loops_limit is not None:
            self._blocking = True
        if 'process_type' in worker_cfg:
            process_type = worker_cfg.get('process_type')

        if process_type is not None:
            if process_type.lower() not in ['fork', 'thread', 'kthread']:
                logger.error(f'Error in {func_name}: unknown process_type "{process_type}"...')
                return

        if 'project' in worker_cfg:
            database.project = worker_cfg.get('project')

        if create_db_worker:
            self._worker = database.get_new_worker()

        database.close_session()

        self._started = True
        self._started_timestamp = datetime.datetime.now()
        if self._blocking:
            loops_counter = 0
            while self._started:
                self._do_tasks(process_type, task_limit)
                loops_counter += 1
                if loops_limit and loops_counter >= loops_limit:
                    logger.info(f'{func_name}; loops_counter({loops_counter})'
                                f' == loops_limit({loops_limit}) => break...')
                    break
                if self._life_timeout_sec is not None:
                    time_delta = datetime.datetime.now() - self._started_timestamp
                    time_delta_sec = time_delta.total_seconds()
                    if time_delta_sec > self._life_timeout_sec:
                        logger.info(f'{func_name}; time_delta_sec({time_delta_sec})'
                                    f' > life_timeout_sec({self._life_timeout_sec}) => break...')
                        break
                if self._sleep_sec is not None:
                    time.sleep(self._sleep_sec)
            if self._worker:
                self._worker.status = 'finished'
                self._worker.finished_time = datetime.datetime.now()
                database.session.commit()
        else:
            self._do_tasks(process_type, task_limit)
            # self._do_task(process_type)

    def stop(self):
        self._started = False


if __name__ == '__main__':
    name = 'Worker'
    ver = '1.3'
    release_date = '2020-06-08 06:00'
    version = f'{name}. ver: {ver} ({release_date})'
    from pg_tasks_queue.Logging import init_logger
    init_logger()

    logger.warning(f'Start {version}')
    Worker().start(config.cfg, config_id=1)
    logger.warning(f'End {version}')


