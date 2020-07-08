# -*- coding: utf-8 -*-

import requests


class HTTP():
    def post(self, headers, params):
        res = requests.post(
            self.url,
            headers=headers,
            data=params
        )

        return res

    def get(self, headers, params):
        res = requests.get(
            self.url,
            headers=headers,
            data=params
        )

        return res

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

