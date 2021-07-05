import unittest
from fastapi.testclient import TestClient

from core.api.controller import create_app
from core.api.request.judge_request import JudgeRequest
from core.api.request.eval_request import EvalRequest
from core.api.request.reading_request import ReadingRequest


class TestAPI(unittest.TestCase):
    DAJARE_JUDGE_PATH: str = '/judge'
    DAJARE_EVAL_PATH: str = '/eval'
    DAJARE_READING_PATH: str = '/reading'

    SAMPLE_STR: str = '布団が吹っ飛んだ'

    def setUp(self):
        self.app = TestClient(create_app())

    def test_正_ダジャレを判定(self):
        # setup
        request_body = JudgeRequest(dajare=self.SAMPLE_STR)

        # test
        res = self.app.get(self.DAJARE_JUDGE_PATH, params=request_body)
        res_json: dict = res.json()

        # verify
        self.assertEqual(200, res.status_code)
        self.assertIsInstance(res_json["is_dajare"], bool)

    def test_異_判定APIのパラメータが不足(self):
        # test
        res = self.app.get(self.DAJARE_JUDGE_PATH, params={})

        # verify
        self.assertEqual(422, res.status_code)

    def test_正_ダジャレを評価(self):
        # setup
        request_body = EvalRequest(dajare=self.SAMPLE_STR)

        # test
        res = self.app.get(self.DAJARE_EVAL_PATH, params=request_body)
        res_json: dict = res.json()

        # verify
        self.assertEqual(200, res.status_code)
        self.assertIsInstance(res_json["score"], float)

    def test_異_評価APIのパラメータが不足(self):
        # test
        res = self.app.get(self.DAJARE_EVAL_PATH, params={})

        # verify
        self.assertEqual(422, res.status_code)

    def test_正_ダジャレを読みに変換(self):
        # setup
        request_body = ReadingRequest(dajare=self.SAMPLE_STR)

        # test
        res = self.app.get(self.DAJARE_READING_PATH, params=request_body)
        res_json: dict = res.json()

        # verify
        self.assertEqual(200, res.status_code)
        self.assertIsInstance(res_json["reading"], str)

    def test_異_読み変換APIのパラメータが不足(self):
        # test
        res = self.app.get(self.DAJARE_READING_PATH, params={})

        # verify
        self.assertEqual(422, res.status_code)
