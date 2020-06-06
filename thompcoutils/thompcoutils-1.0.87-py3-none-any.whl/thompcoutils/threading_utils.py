import threading
import time
import datetime
from thompcoutils.log_utils import get_logger

_time_format = '%H:%M:%S'


def _test1(name, value1, value2):
    print("thread {} starting at {}".format(name, datetime.datetime.now().strftime(_time_format)))
    time.sleep(2)
    print("thread {} done at {}".format(name, datetime.datetime.now().strftime(_time_format)))
    value1 *= 5
    value2 *= 2
    return value1, value2


def _test2(name, value1):
    print("thread {} starting at {}".format(name, datetime.datetime.now().strftime(_time_format)))
    time.sleep(1)
    print("thread {} done at {}".format(name, datetime.datetime.now().strftime(_time_format)))
    value1 *= 3
    return value1


class ThreadManager (threading.Thread):
    THREAD_LOCK = threading.Lock()
    threads = {}

    def __init__(self, name, function, *argv):
        threading.Thread.__init__(self)
        self.name = name
        self.function = function
        self.args = argv
        self.rtn = None
        ThreadManager.threads[name] = self

    def run(self):
        self.rtn = self.function(*self.args)

    @staticmethod
    def start_thread(thread_name):
        ThreadManager.threads[thread_name].start()

    @staticmethod
    def start_all_threads():
        for thread_name in ThreadManager.threads:
            ThreadManager.threads[thread_name].start()

    @staticmethod
    def join_all_threads():
        for thread_name in ThreadManager.threads:
            ThreadManager.threads[thread_name].join()

    @staticmethod
    def join_thread(thread_name):
        ThreadManager.threads[thread_name].join()


def _parameter_function(name):
    return str(name).split("bound method ", 1)[1].split(" of", 1)[0]


class WorkerThread(threading.Thread):
    def __init__(self, callback_function, sleep=None, count=None, parameters=None):
        super(WorkerThread, self).__init__()
        logger = get_logger()
        logger.debug("creating a WorkerThread")
        self.is_running = True
        self.function = callback_function
        self.sleep = sleep
        self.count = count
        self.parameters = parameters

    def run(self):
        logger = get_logger()
        logger.debug("starting WorkerThread")
        self.is_running = True
        while self.is_running:
            if self.parameters is None:
                logger.debug("calling function {}()".format(self.function))
                self.is_running = True
                self.function()
            else:
                logger.debug("calling function {}({})".format(self.function, self.parameters))
                self.function(self.parameters)
            if self.sleep is not None:
                time.sleep(self.sleep)
            if self.count is not None:
                self.count -= 1
                if self.count == 0:
                    self.stop()

    def stop(self):
        self.is_running = False


def _timeout_function(watchdog):
    print('{} Test timeout function called'.format(datetime.datetime.now()))
    watchdog.stop()


class Watchdog(threading.Thread):
    def __init__(self, check_period, timeout_function):
        super(Watchdog, self).__init__()
        self.last_tickle = None
        self.is_running = False
        self.check_period = check_period
        self.timeout_function = timeout_function

    def tickle(self):
        self.last_tickle = datetime.datetime.now()

    def stop(self):
        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running:
            time.sleep(self.check_period)
            now = datetime.datetime.now()
            time_diff = now - self.last_tickle
            if time_diff.seconds > self.check_period:
                self.timeout_function(self)


def _worker_function():
    print('{} running _worker_thread'.format(datetime.datetime.now()))


def _main():
    logger = get_logger()
    thread_test = False
    worker_thread_test = True
    watchdog_test = False

    if worker_thread_test:
        print('{} workerThread_test starting'.format(datetime.datetime.now()))
        worker_thread = WorkerThread(_worker_function, 1, 4)
        worker_thread.start()
        time.sleep(5)
        worker_thread.stop()
        print('{} done'.format(datetime.datetime.now()))

    if watchdog_test:
        logger.warning('{} watchdog_test starting...'.format(datetime.datetime.now()))
        watchdog = Watchdog(2, _timeout_function)
        watchdog.start()
        for i in range(0, 2):
            time.sleep(1)
            logger.warning('{} tickling'.format(datetime.datetime.now()))
            watchdog.tickle()
        time.sleep(2)
        logger.warning('{} watchdog_test done...'.format(datetime.datetime.now()))

    if thread_test:
        # You can use the ThreadManager to take care of the threads for you:
        print('{} thread_test starting'.format(datetime.datetime.now()))
        ThreadManager('one', _test1, 'one', 1, 2)
        ThreadManager('two', _test1, 'two', 3, 4)
        ThreadManager('three', _test2, 'three', 5)
        ThreadManager.start_all_threads()
        print('main starting work at {}'.format(datetime.datetime.now().strftime(_time_format)))
        time.sleep(1)
        print('main done working at {}'.format(datetime.datetime.now().strftime(_time_format)))
        ThreadManager.join_all_threads()

        for thread in ThreadManager.threads:
            print(ThreadManager.threads[thread].rtn)
        print("Back to Main Thread")

        # Or you can manage them yourself:
        thread1 = ThreadManager('one', _test1, 'one', 1, 2)
        thread2 = ThreadManager('two', _test1, 'two', 3, 4)
        thread3 = ThreadManager('three', _test2, 'three', 5)
        thread1.start()
        thread2.start()
        thread3.start()
        print('main starting work at {}'.format(datetime.datetime.now().strftime(_time_format)))
        time.sleep(1)
        print('main done working at {}'.format(datetime.datetime.now().strftime(_time_format)))
        thread1.join()
        thread2.join()
        thread3.join()
        print(thread1.rtn)
        print(thread2.rtn)
        print(thread3.rtn)
        print("Back to Main Thread")
        print('{} thread_test done'.format(datetime.datetime.now()))


if __name__ == '__main__':
    _main()
