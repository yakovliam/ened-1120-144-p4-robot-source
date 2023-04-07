import _thread
from pybricks.tools import wait

class CancellationToken:
   def __init__(self):
       self.is_cancelled = False

   def cancel(self):
       self.is_cancelled = True

class ThreadActionManager:
    default_callback = (
        lambda: print("default callback")
    )
    def __init__(self, main_action: callable, dependent_action: callable, callback=default_callback, should_restart_after_end=False):
        self.main_action = main_action
        self.dependent_action = dependent_action
        self.callback = callback
        self.cancellation_token = CancellationToken()
        self.should_restart_after_end = should_restart_after_end

    def __do_main_action(self):
        self.main_action()

        while not self.cancellation_token.is_cancelled:
            wait(1000)
            pass

    def __do_dependent_action(self):
        self.dependent_action()
        self.end()

    def start(self):
        while True:
            _thread.start_new_thread(self.__do_dependent_action, ())
            self.__do_main_action()
            if not self.should_restart_after_end:
                break


    def end(self):
        self.cancellation_token.cancel()
        self.callback()        

