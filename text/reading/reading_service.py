# -*- coding: utf-8 -*-


class ReadingService():
    def __init__(self):
        from .withapi import WithAPI
        from .withoutapi import WithoutAPI
        self.conv_with_api = WithAPI()
        self.conv_without_api = WithoutAPI()

    def convert(self, text, use_api=True):
        result = ''
        api_status = False

        if use_api:
            result, api_status = self.conv_with_api.text_to_reading(text)

        if not api_status:
            result = self.conv_without_api.text_to_reading(text)[0]

        return result
