import _thread
from idgenerator import generate_id
from pybricks.tools import wait

class CancellationToken:
   def __init__(self):
       self.is_cancelled = False

   def cancel(self):
       self.is_cancelled = True
       
class DoUntil:
    actions = {}

    def __init__(self):
        pass

    def _construct_do_cancellation_dependent_action(self, do_callable: callable, task_id: str, delay_ms=0):
        while task_id in self.actions:
            try:
                if self.actions[task_id].is_cancelled:
                    break
            except:
                pass

            do_callable()

            if delay_ms > 0:
                wait(delay_ms)

    def _construct_do_action(self, do_callable: callable, task_id: str, callback=lambda: ()):
        do_callable()
        # remove the action from the actions map
        del self.actions[task_id]
        callback()
        
    def _construct_until_action(self, until_callable: callable, do_task_id: str, callback=lambda: ()):
        count = 0
        while True:
            if until_callable():
                break
            wait(100)
            count += 1
        self.actions[do_task_id].cancel()
        # remove the action from the actions map
        del self.actions[do_task_id]
        callback()


    def do_until(self, do_callable: callable, until_callable: callable, callback=lambda: (), blocking=False, do_callable_delay_ms=0) -> str:
        # generate random task id
        task_id = generate_id(10)
        # add the action to the actions map using a cancellable token
        self.actions[task_id] = CancellationToken()
        _thread.start_new_thread(self._construct_until_action, (until_callable, task_id, callback))

        # start the do callable on the main thread
        self._construct_do_cancellation_dependent_action(do_callable, task_id, do_callable_delay_ms)

        if blocking:
            while task_id in self.actions:
                wait(100)

        return task_id

    def do(self, do_callable: callable, callback=lambda: (), blocking=False) -> str:
        # generate random task id
        task_id = generate_id(10)
        # add the action to the actions map using a cancellable token
        self.actions[task_id] = CancellationToken()
        _thread.start_new_thread(self._construct_do_action, (do_callable, task_id, callback))

        if blocking:
            while task_id in self.actions:
                wait(100)

        return task_id

singleton_do_until = DoUntil()