from flask import request
from flask_restful import Resource


class API(Resource):
    def catch_req(self):
        result = {"status": "OK", "message": "success"}
        args = {}
        if request.method == 'GET':
            args = request.args
        if request.method == 'POST':
            args = request.json

        try:
            if self._args_validation(args):
                result.update(self._processing(args))
                return result, 200
            else:
                result["status"] = "error"
                result["message"] = "parameter is missing"
                return result, 400

        except Exception as e:
            result["status"] = "error"
            result["message"] = str(e)
            return result, 500

    def get(self):
        return self.catch_req()

    def post(self):
        return self.catch_req()

    def _args_validation(self, arg):
        raise Exception('サブクラスの責務')

    def _processing(self, args):
        raise Exception('サブクラスの責務')
