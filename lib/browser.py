# Date: 25/10/2023
# Author: Mr.X
# Description: Browser

import contextlib
from time import time

import requests


class Browser(object):

    def __init__(self, link):
        self.link = link
        self.is_active = True
        self.start_time = None
        self.is_vulner = False
        self.is_attempted = False

    def get_content(self):
        with contextlib.suppress(Exception):
            return requests.get(f'{self.link}*').text.lower()

    def attempt(self):
        self.start_time = time()
        if content := self.get_content():
            self.is_attempted = True

            if 'sql' in content and 'error' in content and 'at line' in content:
                self.is_vulner = True

        self.is_active = False