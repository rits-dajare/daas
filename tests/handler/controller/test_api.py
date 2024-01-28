import unittest
from fastapi.testclient import TestClient

from app.handler.controller.outer import fastapi_app
from app.handler.dto.eval_dto import EvalV1
from app.handler.dto.judge_dto import JudgeV1
from app.handler.dto.reading_dto import ReadingV1


class TestAPI(unittest.TestCase):
    DAJARE_JUDGE_PATH: str = '/judge'
    DAJARE_EVAL_PATH: str = '/eval'
    DAJARE_READING_PATH: str = '/reading'

    SAMPLE_STR: str = '布団が吹っ飛んだ'

    def setUp(self):
        self.app = TestClient(fastapi_app())

    def test_正_ダジャレを判定(self):
        # setup
        request_body = JudgeV1.Request(dajare=self.SAMPLE_STR)

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
        request_body = EvalV1.Request(dajare=self.SAMPLE_STR)

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
        request_body = ReadingV1.Request(dajare=self.SAMPLE_STR)

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
