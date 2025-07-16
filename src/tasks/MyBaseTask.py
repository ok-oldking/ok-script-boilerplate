import re

from ok import BaseTask

class MyBaseTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def operate(self, func):
        self.executor.interaction.operate(func, block=True)

    def do_mouse_down(self, key):
        self.executor.interaction.do_mouse_down(key=key)

    def do_mouse_up(self, key):
        self.executor.interaction.do_mouse_up(key=key)

    def do_send_key_down(self, key):
        self.executor.interaction.do_send_key_down(key)

    def do_send_key_up(self, key):
        self.executor.interaction.do_send_key_up(key)



