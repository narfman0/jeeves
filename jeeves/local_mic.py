# -*- coding: utf-8 -*-
"""
A drop-in replacement for the Mic class that allows for all I/O to occur
over the terminal. Useful for debugging. Unlike with the typical Mic
implementation, we are always active listening with local_mic.
"""


class Mic(object):
    prev = None

    def __init__(self, *args, **kwargs):
        return

    def wait_for_keyword(self, keyword="JEEVES"):
        return

    def active_listen(self, timeout=3):
        input = raw_input("YOU: ")
        self.prev = input
        return [input]

    def listen(self):
        return self.active_listen(timeout=3)

    def say(self, phrase, OPTIONS=None):
        print("JEEVES: %s" % phrase)
