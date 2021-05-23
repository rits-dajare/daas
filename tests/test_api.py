import unittest
from fastapi.testclient import TestClient

from core.api.controller import create_app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = TestClient(create_app())

    def test_正_ダジャレを判定(self):
        res = self.app.get('judge', params={'dajare': '布団が吹っ飛んだ'})
        res_json: dict = res.json()

        self.assertEqual(200, res.status_code)
        self.assertIsInstance(res_json["is_dajare"], bool)

    def test_異_判定APIのパラメータが不足(self):
        res = self.app.get('judge', params={})
        self.assertEqual(422, res.status_code)

    def test_正_ダジャレを評価(self):
        res = self.app.get('eval', params={'dajare': '布団が吹っ飛んだ'})
        res_json: dict = res.json()

        self.assertEqual(200, res.status_code)
        self.assertIsInstance(res_json["score"], float)

    def test_異_評価APIのパラメータが不足(self):
        res = self.app.get('eval', params={})
        self.assertEqual(422, res.status_code)

    def test_正_ダジャレを読みに変換(self):
        res = self.app.get('reading', params={'dajare': '布団が吹っ飛んだ'})
        res_json: dict = res.json()

        self.assertEqual(200, res.status_code)
        self.assertIsInstance(res_json["reading"], str)

    def test_異_読み変換APIのパラメータが不足(self):
        res = self.app.get('reading', params={})
        self.assertEqual(422, res.status_code)
