import threading


class Timer:

    def __init__(self, period_ms, function, args):
        self.period_ms = period_ms
        self.function = function
        self.args = args

        self.timer = self._create_timer_thread(self.period_ms)
        self.timer.start()

    def _create_timer_thread(self, period_ms):
        thread = threading.Timer(period_ms / 1000., self._run, )
        thread.setDaemon(True)
        return thread

    def _run(self):
        self.function(*self.args)
        self.timer = self._create_timer_thread(self.period_ms)
        self.timer.start()
