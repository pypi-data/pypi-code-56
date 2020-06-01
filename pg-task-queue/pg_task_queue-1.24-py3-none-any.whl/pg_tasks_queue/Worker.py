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
import Common.Kthread as kthread

# from Common.Database import TasksDatabase as _database
from Common.Config import cfg as config
import Common.Database as database


import logging
logger = logging.getLogger(__name__)


class Worker:

    _blocking = False
    _sleep_sec = 1.
    _timeout_sec = 60.
    _life_timeout_sec = None
    _started = False
    _started_timestamp = None
    _worker = None
    _current_task = None
    _raise_exception = True

    def check_module(self, module_name):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'
        module_spec = importlib.util.find_spec(module_name)
        if module_spec is None:
            print(f'Error in {func_name}: module: "{module_name}" not found')
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
                timer = threading.Timer(self._timeout_sec, self.stop_woker, args=(func_name,))
                timer.setDaemon(False)
                timer.start()
                result_dict = self.worker(task_dict)
                timer.cancel()
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
                        worker = kthread.KThread(target=self.worker_process, args=(worker_queue, task_dict,))
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
            database.set_worker_error(error, self._worker, self._current_task)
        finally:
            if self._raise_exception and exception:
                raise exception
            else:
                if isinstance(error, str):
                    logger.error(error)
            if not self._blocking:
                if self._life_timeout_sec is not None:
                    time_delta = datetime.datetime.now() - self._started_timestamp
                    time_delta_sec = time_delta.total_seconds()
                    if time_delta_sec > self._life_timeout_sec:
                        logger.info(f'{func_name}; time_delta_sec({time_delta_sec})'
                                    f' > life_timeout_sec({self._life_timeout_sec}) => return...')
                        return
                threading.Timer(self._sleep_sec, self._do_task, args=(process_type,)).start()

    def start(self):
        func_name = f'{self.__class__.__name__}.{sys._getframe().f_code.co_name}()'

        if not isinstance(config.cfg, dict):
            logger.error(f'Error in {func_name}: not isinstance(config.cfg, dict); return...')
            return

        if not database.init():
            logger.error(f'Error in {func_name}: not models.init()...')
            return

        process_type = None
        loops_limit = None
        worker_cfg = config.cfg.get('worker')

        if isinstance(worker_cfg, dict):

            self._blocking = worker_cfg.get('blocking', False)

            if worker_cfg.get('raise_exception') is not None:
                self._raise_exception = worker_cfg.get('raise_exception')

            if worker_cfg.get('sleep_sec') is not None:
                self._sleep_sec = float(worker_cfg.get('sleep_sec'))

            if worker_cfg.get('timeout_sec') is not None:
                self._timeout_sec = float(worker_cfg.get('timeout_sec'))

            if worker_cfg.get('life_timeout_sec') is not None:
                self._life_timeout_sec = float(worker_cfg.get('life_timeout_sec'))

            if worker_cfg.get('loops_limit') is not None:
                loops_limit = int(worker_cfg.get('loops_limit'))
                self._blocking = True

            if worker_cfg.get('process_type') is not None:
                process_type = worker_cfg.get('process_type')

        if process_type is not None:
            if process_type.lower() not in ['fork', 'thread', 'kthread']:
                logger.error(f'Error in {func_name}: unknown process_type "{process_type}"...')
                return

        self._worker = database.get_new_worker()
        self._started = True
        self._started_timestamp = datetime.datetime.now()
        if self._blocking:
            loops_counter = 0
            while self._started:
                self._do_task(process_type)
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
                time.sleep(self._sleep_sec)
        else:
            self._do_task(process_type)

    def stop(self):
        self._started = False


if __name__ == '__main__':
    name = 'Worker'
    ver = '1.0'
    release_date = '2020-06-01 09:24'
    version = f'{name}. ver: {ver} ({release_date})'
    from Common.Logging import init_logger
    init_logger()

    logger.warning(f'Start {version}')
    Worker().start()
    logger.warning(f'End {version}')


