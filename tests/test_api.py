import unittest


class TestAPI(unittest.TestCase):
    def setUp(self):
        from core.api import controller
        self.app = controller.create_app().test_client()

    def test_正_ダジャレを判定(self):
        res = self.app.get('judge/', query_string={'dajare': '布団が吹っ飛んだ'})
        self.assertEqual(200, res.status_code)

    def test_異_判定APIのパラメータが不足(self):
        res = self.app.get('judge/', query_string={})
        self.assertEqual(400, res.status_code)

    def test_正_ダジャレを評価(self):
        res = self.app.get('eval/', query_string={'dajare': '布団が吹っ飛んだ'})
        self.assertEqual(200, res.status_code)

    def test_異_評価APIのパラメータが不足(self):
        res = self.app.get('eval/', query_string={})
        self.assertEqual(400, res.status_code)

    def test_正_ダジャレを読みに変換(self):
        res = self.app.get('reading/', query_string={'dajare': '布団が吹っ飛んだ'})
        self.assertEqual(200, res.status_code)

    def test_異_読み変換APIのパラメータが不足(self):
        res = self.app.get('reading/', query_string={})
        self.assertEqual(400, res.status_code)
