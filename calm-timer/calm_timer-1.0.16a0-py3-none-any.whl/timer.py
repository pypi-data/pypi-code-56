from PyQt5 import QtCore
import logging
import ct.ct_global


class Timer(QtCore.QObject):
    update_signal = QtCore.pyqtSignal(bool)
    # -list has a collection of IDs, bool is whether it's a missed notification

    def __init__(self):
        super().__init__()

        self.secs_remaining_int = 0
        self.start_secs_int = -1
        self.second_qtimer = None

    def start(self, i_time: int):
        self.start_secs_int = i_time
        self.secs_remaining_int = i_time
        self.stop()
        self.second_qtimer = QtCore.QTimer(self)
        self.second_qtimer.timeout.connect(self.timeout)
        time_int = 1000
        if ct.ct_global.testing_bool:
            time_int = 50
        self.second_qtimer.start(time_int)  # -one second

    def stop(self):
        if self.second_qtimer is not None and self.second_qtimer.isActive():
            self.second_qtimer.stop()
        self.secs_remaining_int = self.start_secs_int
        self.update_signal.emit(False)
        # update_gui()

    def is_active(self):
        if self.second_qtimer is None:
            return False
        ret_is_active_bool = self.second_qtimer.isActive()
        return ret_is_active_bool

    def timeout(self):
        """
        Function is called every minute
        """
        self.secs_remaining_int -= 1
        # logging.debug("time_remaining " + str(self.secs_remaining_int))
        completed_bool = False
        if self.secs_remaining_int == 0:
            completed_bool = True
            self.stop()

        self.update_signal.emit(completed_bool)



