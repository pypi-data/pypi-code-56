from threading import Thread


class Runnable(Thread):
    do_run = False

    def __init__(self, **kwargs):
        Thread.__init__(self)
        if kwargs is not None:
            self.__dict__.update(kwargs)
        self.do_run = True

    def run(self) -> None:
        self.on_start()
        while self.do_run:
            self.work()
        self.on_stop()

    def stop(self):
        self.do_run = False

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def work(self):
        pass
