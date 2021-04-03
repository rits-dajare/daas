import unittest


class TestAPI(unittest.TestCase):
    def setUp(self):
        from webapi import create_app
        self.app = create_app().test_client()

    def test_judge(self):
        res = self.app.get('judge/', query_string={'dajare': '布団が吹っ飛んだ'})
        self.assertEqual(200, res.status_code)

    def test_eval(self):
        res = self.app.get('eval/', query_string={'dajare': '布団が吹っ飛んだ'})
        self.assertEqual(200, res.status_code)

    def test_reading(self):
        res = self.app.get('reading/', query_string={'dajare': '布団が吹っ飛んだ'})
        self.assertEqual(200, res.status_code)
