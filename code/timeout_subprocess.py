import subprocess as sub
import threading, time

def run_with_timeout(func, args=(), timeout_duration=1, default="timeout"):
    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(timeout_duration)
    try:
        result = func(*args)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)

    return result
  