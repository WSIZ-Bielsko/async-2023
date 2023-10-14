import threading
from asyncio import current_task
from datetime import datetime


def ts():
    return datetime.now().timestamp()


def thread_name():
    return threading.current_thread().name


def task_name():
    return current_task().get_name()

